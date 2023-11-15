"""
session.py 

"""

from contextlib import contextmanager
from io import SEEK_SET
from os import PathLike
import os.path
from typing import Any, Optional, Dict, BinaryIO

from wavinfo.reader.riff_parser import (ChunkDescriptor, ListChunkDescriptor, 
                                        parse_chunk)
from wavinfo.writer.wave_writer import WavInfoWriter

from .scopes import bext, adm, dbmd, ixml, info, cues


@contextmanager 
def open_wavinfo(*args, **kwargs):
    """
    Opens a new WavInfo object and closes it when finished it, writing any
    changes made.
    """
    wi = WavInfo(*args, **kwargs)
    try:
        yield wi 
    except Exception as e:
        print(f"Exception thrown in {open_wavinfo.__name__} with args={args}, "
              "kwargs={kwargs}")
        raise e
    finally:
        wi.close()


class _WavInfoLoaderImpl:

    @staticmethod
    def read_chunk(f: BinaryIO, chunk_ident: bytes) -> Optional[bytes]:
        assert len(chunk_ident) == 4
        f.seek(0, SEEK_SET)
        main_list = parse_chunk(f)
        assert isinstance(main_list, ListChunkDescriptor)
        chunk = next((c for c in main_list.children 
                      if c.ident == chunk_ident 
                      and isinstance(c, ChunkDescriptor)), None)

        assert isinstance(chunk, ChunkDescriptor)
        return chunk.read_data(f)

    @staticmethod
    def load_bext(f: BinaryIO) -> Optional[bext.Bext]:
        data = _WavInfoLoaderImpl.read_chunk(f, b"bext")
        return bext.read(bext_data=data, encoding='ascii') if data else None
        


class WavInfo:
    def __init__(self, f) -> None:
        self._scopes_cache: Dict[str, Any] = { 'bext': None, 'adm': None,
                                              'dbmd': None, 'ixml': None,
                                              'cues': None, 'info': None }

        self._touched_scopes = dict()
        for key in self._scopes_cache.keys():
            self._touched_scopes[key] = False

        self.f = f 

    def _load_all(self):
        with self._open_f_for_reading() as file:
            for scope in self._scopes_cache.keys():
                self._load_scope(scope, file)

    @contextmanager
    def _open_f_for_reading(self):
        if hasattr(self.f, 'read'):
            yield self.f
        elif isinstance(self.f, PathLike):
            with open(self.f, 'rb') as file:
                yield file

    def _load_scope(self, scope: str, f: BinaryIO):
        if scope == 'bext':
            self._scopes_cache['bext'] = _WavInfoLoaderImpl.load_bext(f)

    def write_all(self):
        """
        Write all unwritten changes. 
        """
        pass

    def close(self):
        """
        Writes any unwritten changes to the file anc closes it.
        """
        self.write_all()


