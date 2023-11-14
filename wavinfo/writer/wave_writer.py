"""
wave_writer.py

"""

# from typing_extensions import Buffer
from ..reader.riff_parser import (parse_chunk, ChunkDescriptor, 
                                  ListChunkDescriptor)

from enum import Enum
from struct import pack, unpack
from io import SEEK_END, BufferedRandom, SEEK_CUR, SEEK_SET
from typing import Tuple, Optional

JUNK_IDENTS = (b'JUNK', b'FLLR', b'PAD ')


class WavInfoWriter:
    """
    An in-place WAVE file chunk writer/updater.
    """

    #: Size of initial ``JUNK`` chunk to avoid overwriting.
    ds64_reservation_size: int = 64
    preserve_ds64_reservation: bool = True
    file: BufferedRandom

    class Placement(Enum):
        #: Place new chunk as early in the file as possible.
        FIRST_AVAILABLE = 1

        #: Place new chunk after `data`
        AFTER_DATA = 2


    def __init__(self, f):
        if hasattr(f, 'read') and hasattr(f, 'write'):
            self.file = f
        else:
            self.file = open(f, "r+b")

        self.file.seek(0, SEEK_SET)
        main_list = parse_chunk(self.file)
        assert isinstance(main_list, ListChunkDescriptor)
        assert not main_list.is_rf64(), ("RF64 metadata writing is not "
                                         "supported")

    def erase_chunk(self, ident: bytes, index: int):
        """
        Strike-out a chunk with a ``JUNK`` chunk, and then combine with
        adjacent ``JUNK`` if there.
        """
        self.file.seek(0, SEEK_SET)
        main_list = parse_chunk(self.file)
        assert isinstance(main_list, ListChunkDescriptor)

        i = 0
        for chunk in main_list.children:
            if not isinstance(chunk, ChunkDescriptor):
                continue
            if chunk.ident == ident:
                if i == index:
                    self.file.seek(chunk.start - 8, SEEK_SET)
                    self.file.write(b"JUNK")
                else:
                    i += 1

        self.file.flush()
        self._combine_adjacent_junk()
        self._truncate_tail_junk()

    def erase_list_form(self, ident: bytes, index: int):
        """
        Strike-out a ``LIST`` chunk form with a signature ``ident``.
        """
        self.file.seek(0, SEEK_SET)
        main_list = parse_chunk(self.file)
        assert isinstance(main_list, ListChunkDescriptor)

        i = 0
        for chunk in main_list.children:
            if not isinstance(chunk, ListChunkDescriptor):
                continue
            if chunk.signature == ident:
                if i == index:
                    self.file.seek(chunk.start - 8, SEEK_SET)
                    self.file.write(b"JUNK")
                else:
                    i += 1

        self.file.flush()
        self._combine_adjacent_junk()
        self._truncate_tail_junk()

    def write_chunk(self, ident: bytes, data: bytes,
                    placement: Placement = Placement.FIRST_AVAILABLE):
        """
        Writes a new chunk
        """
        if placement == self.Placement.FIRST_AVAILABLE:
            target = self._first_available_junk(sized_for=len(data))
            if target is not None:
                if target[1] is True:
                    self._overwrite_junk(target[0], ident, data)
                else:
                    self._split_junk(target[0], len(data))
                    self._overwrite_junk(target[0], ident, data)

        elif placement == self.Placement.AFTER_DATA:
            pass

        self._combine_adjacent_junk()
        self._truncate_tail_junk()

    def _first_available_junk(self,
                              sized_for: int) -> Optional[Tuple[int, bool]]:
        """
        Find the first available ``JUNK`` large enough to for free space to be
        allocated to a chunk of size ``sized_for``. A ``JUNK`` chunk is
        available if it can be split into a chunk ``sized_for``

        :returns: index of found chunk, and bool indicating if the size match
            is exact.
        """
        junks = self._junk_list()
        for i, junk in enumerate(junks):
            if self._can_split_junk(i, sized_for):
                return i, False
            elif junk.length in [sized_for, sized_for + 1]:
                return i, True

        return None

    def _split_junk(self, index: int, at: int):
        """
        Split a ``JUNK`` chunk. After splitting, file will have two ``JUNK``
        chunks, one at ``index`` and one at ``index + 1``.

        ``JUNK`` at ``index`` will have size ``at + (at % 2)``, all remaining
        space (mins 8 bytes of chunk overhead) will be allocated to ``JUNK``
        at ``index + 1``. This space must be greater than or equal to the
        minimum chunk size, two bytes, and this is asserted. To check this
        without an assertion use ``_can_split_junk()``.
        """
        assert self._can_split_junk(
            index, at), (f"Cannot split JUNK chunk at "
                         "index {index}, insufficient remaining size")

        target = self._get_junk_at(index)

        self.file.seek(target[0] - 4, SEEK_SET)
        head_size = at + at % 2
        tail_size = target[1] - (head_size + 8)
        self.file.write(pack("<I", head_size))
        self.file.seek(head_size, SEEK_CUR)
        self.file.write(b"JUNK")
        self.file.write(pack("<I", tail_size))
        self.file.flush()

    def _can_split_junk(self, index: int, at: int) -> bool:
        """
        Tests if the ``JUNK`` chunk at ``index`` can be split at position
        ``at``, and leave enough space for the second. ``at`` will be rounded
        up to the nearest even number.
        """
        target = self._get_junk_at(index)

        assert at > 0, f"Cannot split chunk at index 0"

        MIN_JUNK_SIZE = 2
        HEADER_SIZE = 8
        target_len = target[1]
        size_head = at + at % 2
        size_tail = target_len - (size_head + HEADER_SIZE)

        return size_tail >= MIN_JUNK_SIZE

    def _get_junk_at(self, index: int) -> Tuple[int, int]:
        """
        Get the location of a ``JUNK`` chunk.

        :param index: The index of the ``JUNK`` chunk to find.
        :returns: A Tuple with the offset of the requested ``JUNK`` chunk's
            payload, and the length of the payload.
        """
        junks = self._junk_list()

        assert len(junks) > index, f"No JUNK chunk at index {index}"

        return (junks[index].start, junks[index].length)

    def _get_tail_junk(self) -> Optional[Tuple[int, int]]:
        """
        Returns the start and size of the last junk chunk, if nothing follows
        if
        """
        self.file.seek(0, SEEK_SET)
        main_list = parse_chunk(self.file)
        assert isinstance(main_list, ListChunkDescriptor)
        if len(main_list.children) == 0: return
        if main_list.children[-1].ident in JUNK_IDENTS:
            return (main_list.children[-1].start, 
                    main_list.children[-1].length)


    def _overwrite_junk(self, index: int, new_ident: bytes, data: bytes):
        """
        Overwrite a ``JUNK`` chunk. The chunk overwritten must be exactly
        ``len(data)`` size, or one more than ``len(data)``.
        """
        target = self._get_junk_at(index)
        assert len(data) in (target[1], target[1] - 1), \
            (f"JUNK chunk at index {index} is not correct size for data len "
             "{len(data)}")

        self.file.seek(target[0] - 8, SEEK_SET)
        self.file.write(new_ident)
        self.file.write(pack("<I", len(data)))
        self.file.write(data)
        self.file.flush()

    def _append_chunk(self, new_ident, data: bytes):
        """
        Append a new chunk at the end of the file.
        """
        self.file.seek(0, SEEK_SET)
        main_list = parse_chunk(self.file)
        assert isinstance(main_list, ListChunkDescriptor)
        assert False, "Implementation in progress"  # FIXME

    def _combine_adjacent_junk(self):
        """
        Combine adjacent ``JUNK`` chunks into single chunks.
        """
        l = self._junk_list()
        if len(l) == 1:
            return

        i = 0
        while i + 1 < len(self._junk_list()):
            (a, b) = (self._get_junk_at(i), self._get_junk_at(i + 1))
            if a[0] + a[1] + 8 == b[0]:
                self.file.seek(a[0] - 4, SEEK_SET)
                new_a_size = a[1] + 8 + b[1]
                self.file.write(pack("<I", new_a_size))
                self.file.flush()
            else:
                i += 1

    def _truncate_tail_junk(self):
        """
        Deletes the final chunk from the file if it is a ``JUNK`` chunk.
        """
        tail_junk = self._get_tail_junk()
        if tail_junk is None: return 

        tail_junk_start, tail_junk_size = tail_junk

        self.file.seek(4, SEEK_SET)
        current_file_size = unpack("<I", self.file.read(4))[0]
        self.file.seek(-4, SEEK_CUR)
        self.file.write(pack("<I", 
                             current_file_size - (tail_junk_size + 8)
                             )
                )

        # truncate file
        self.file.truncate(tail_junk_start - 8)




    def _optimize(self):
        """
        Coplete a writing session
        - Calls ``_combine_adjacent_junk()``
        - Deletes all junk at the end of the file.
        """
        pass

    def _junk_list(self):
        self.file.seek(0, SEEK_SET)
        main_list = parse_chunk(self.file)
        assert isinstance(main_list, ListChunkDescriptor)
        return [c for c in main_list.children
                if isinstance(c, ChunkDescriptor) and c.ident in JUNK_IDENTS]
