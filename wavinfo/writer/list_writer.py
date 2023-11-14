from contextlib import contextmanager
from struct import pack
from typing import IO 


@contextmanager 
def write_wave_file(descriptor: IO):
    wf = ListForm(b"RIFF", b"WAVE")
    yield wf
    descriptor.write(wf.finalize())

class ListForm:
    def __init__(self, ident: bytes, signature: bytes) -> None:
        """
        Create a new list form.
        
        :param signature: The signature four-cc of the list form. Must be 
            exactly four bytes.
        """
        assert len(ident) == 4
        assert len(signature) == 4
        self.ident = ident
        self.signature = signature
        self.buffer = signature

    def add_child(self, ident: bytes, data: bytes) -> None:
        """
        Add a new child chunk to the list. 
        """
        assert len(ident) == 4
        self.buffer += ident + pack("<I", len(data)) + data

        if len(data) % 2 == 1:
            self.buffer += b"\0"

    def add_junk(self, length: int):
        junk = b"\0" * length
        self.add_child(b"JUNK", junk)
   
    @contextmanager 
    def child_list(self, signature: bytes):
        child_list = ListForm(b"LIST", signature)
        yield child_list
        self.buffer += child_list.finalize()

    def finalize(self) -> bytes:
        """
        Output a completed RIFF LIST form
        """
        assert len(self.buffer) % 2 == 0
        return self.ident + pack("<I", len(self.buffer)) + self.buffer 
