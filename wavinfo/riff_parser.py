
import struct
import pdb
from collections import namedtuple

class ListChunkDescriptor(namedtuple('ListChunkDescriptor' , 'signature children')):

    def find(chunk_path):
        if len(chunk_path) > 1:
            for chunk in self.children:
                if type(chunk) is ListChunkDescriptor and \
                        chunk.signature is chunk_path[0]:
                            return chunk.find(chunk_path[1:])
        else:
            for chunk in self.children:
                if type(chunk) is ChunkDescriptor and \
                        chunk.ident is chunk_path[0]:
                            return chunk


class ChunkDescriptor(namedtuple('ChunkDescriptor', 'ident start length') ):
    def read_data(self, from_stream):
        from_stream.seek(self.start)
        return from_stream.read(self.length)

def parse_list_chunk(stream, length):
    start = stream.tell()

    signature = stream.read(4)

    children = []
    while (stream.tell() - start) < length:
        child_chunk = parse_chunk(stream)
        if child_chunk:
             children.append(child_chunk)
        else: 
             break

    return ListChunkDescriptor(signature=signature, children=children)

def parse_chunk(stream):
    #breakpoint()
    ident = stream.read(4)
    if len(ident) != 4:
        return

    sizeb = stream.read(4)
    size  = struct.unpack('<I',sizeb)[0]

    displacement = size
    if displacement % 2 is not 0:
        displacement = displacement + 1

    if ident in [b'RIFF',b'LIST']:
        return parse_list_chunk(stream=stream, length=size)
    else:
        start = stream.tell()
        stream.seek(displacement,1)
        return ChunkDescriptor(ident=ident, start=start, length=size)





