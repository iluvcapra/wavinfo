"""
session.py 

"""

from contextlib import contextmanager
from io import SEEK_SET
import pathlib
import os.path
from typing import Optional

from wavinfo.reader.riff_parser import ChunkDescriptor, ListChunkDescriptor, parse_chunk
from wavinfo.writer.wave_writer import WavInfoWriter

from .scopes import bext, adm, dbmd, ixml, info, cues


@contextmanager 
def open_wavinfo(*args, **kwargs):
    wi = WavInfo(*args, **kwargs)
    try:
        yield wi 
    except Exception as e:
        print(f"Exception thrown in WavInfo object with args={args}, "
              "kwargs={kwargs}")
        raise e
    finally:
        wi.close()


class WavInfo:
    def __init__(self, f) -> None:
        self._scopes_cache = { 'bext': None, 'adm': None, 'dbmd': None, 
                              'ixml': None, 'cues': None, 'info': None }

        self._touched_scopes = dict()
        for key in self._scopes_cache.keys():
            self._touched_scopes[key] = False

        self.file = open(f, 'r+b')

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
        self.file.close()


