from struct import pack

class ListForm:
    
    def __init__(self, signature: bytes) -> None:
        """
        Create a new list form.
        
        :param signature: The signature four-cc of the list form. Must be 
            exactly four bytes.
        """
        assert len(signature) == 4
        assert type(signature) == bytes
        self.signature = signature
        self.buffer = signature

    def add_child(self, ident: bytes, data: bytes) -> None:
        """
        Add a new child chunk to the list. 
        """
        assert len(ident) == 4
        self.buffer.join([ident, pack("<I", len(data)), data])

        if len(data) % 2 == 1:
            self.buffer.join([b"\0"])

    def finalize(self) -> bytes:
        """
        Output a completed list form payload (the receiver must place it 
        inside a chunk before adding to a file) 
        """
        return self.buffer 
