
import struct

from collections import namedtuple

ListChunkDescriptor = namedtuple('ListChunkDescriptor' , 'signature children')

class ChunkDescriptor(namedtuple('ChunkDescriptor', 'ident start length') ):
    def read_data(self, from_stream):
        from_stream.seek(self.start)
        return from_stream.read(self.length)


def parse_list_chunk(stream, length):
    children = []

    start = stream.tell()

    signature = stream.read(4)

    while (stream.tell() - start) < length:
        children.append(parse_chunk(stream))

    return ListChunkDescriptor(signature=signature, children=children)


def parse_chunk(stream):
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








        




