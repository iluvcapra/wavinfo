"""
wave_writer.py

"""

from typing_extensions import Buffer
from .riff_parser import parse_chunk, ChunkDescriptor, ListChunkDescriptor

from enum import Enum
from struct import pack
from io import BufferedRandom, SEEK_CUR, SEEK_SET
from typing import Tuple, Optional


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
        HEAD = 1
        
        #: Place new chunk at the end.
        TAIL = 2
   
    def __init__(self, f, preserve_ds64_reservation: bool = True):
        if isinstance(f, BufferedRandom):
            self.file = f
        else:
            self.file = open(f, "r+b")

    def erase_chunk(self, ident: bytes, index: int):
        """
        Strike-out a chunk with a ``JUNK`` chunk, and then combine with 
        adjacent ``JUNK`` if there.
        """
        pass

    def rubout_list_form(self, ident: bytes, index: int):
        """
        Strike-out a ``LIST`` chunk form with a signature ``ident``. 
        """
        pass

    def write_chunk(self, ident: bytes, data: bytes, 
                    placement: Placement = Placement.HEAD):
        """
        Writes a new chunk 
        """
        if placement == self.Placement.HEAD:
            pass
        elif placement == self.Placement.TAIL:
            pass

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
        assert self._can_split_junk(index, at), (f"Cannot split JUNK chunk at "
            "index {index}, insufficient remaining size")

        target = self._get_junk_at(index)

        self.file.seek(target[0] - 4, SEEK_SET)
        head_size = at + at % 2
        tail_size = at - (head_size + 8)
        self.file.write(pack("<H", head_size))
        self.file.seek(at, SEEK_CUR)
        self.file.write(b"JUNK")
        self.file.write(pack("<H", tail_size))
        self.file.flush()
        
    def _can_split_junk(self, index: int, at: int) -> bool:
        """
        Tests if the ``JUNK`` chunk at ``index`` can be split at position 
        ``at``, and leave enough space for the second.
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
        self.file.write(pack("<H", len(data)))
        self.file.write(data)
        self.file.flush()

    def _append_chunk(self, new_ident, data: bytes):
        """
        Append a new chunk at the end of the file.
        """
        pass

    def _rubout_chunk(self, index: int):
        target = self._get_junk_at(index)

        self.file.seek(target[0] - 8, SEEK_SET)
        self.file.write(b"JUNK")
        self.file.flush()

    def _combine_adjacent_junk(self):
        """
        Combine adjacent ``JUNK`` chunks into single chunks.
        """
        pass

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
        return [c for c in main_list 
                if isinstance(c, ChunkDescriptor) and c.ident ==b"JUNK"]
