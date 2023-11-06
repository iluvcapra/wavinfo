
import struct
from collections import namedtuple
from .rf64_parser import parse_rf64


class WavInfoEOFError(EOFError):
    def __init__(self, identifier, chunk_start):
        self.identifier = identifier
        self.chunk_start = chunk_start


class ListChunkDescriptor(namedtuple('ListChunkDescriptor', 'signature children')):
    pass


class ChunkDescriptor(namedtuple('ChunkDescriptor', 'ident start length rf64_context')):
    def read_data(self, from_stream) -> bytes:
        from_stream.seek(self.start)
        return from_stream.read(self.length)


def parse_list_chunk(stream, length, rf64_context=None):
    start = stream.tell()
    signature = stream.read(4)

    children = []
    while stream.tell() - start + 8 < length:
        child_chunk = parse_chunk(stream, rf64_context=rf64_context)
        children.append(child_chunk)

    stream.seek(start + length)

    return ListChunkDescriptor(signature=signature, children=children)


def parse_chunk(stream, rf64_context=None):
    header_start = stream.tell()
    ident = stream.read(4)
    size_bytes = stream.read(4)

    if len(ident) != 4 or len(size_bytes) != 4:
        raise WavInfoEOFError(identifier=ident, chunk_start=header_start)

    data_size = struct.unpack('<I', size_bytes)[0]

    if data_size == 0xFFFFFFFF:
        if rf64_context is None and ident in {b'RF64', b'BW64'}:
            rf64_context = parse_rf64(stream=stream, signature=ident)

        assert rf64_context is not None, \
            f"Sentinel data size 0xFFFFFFFF found outside of RF64 context"
        
        data_size = rf64_context.bigchunk_table[ident]

    displacement = data_size
    if displacement % 2:
        displacement += 1

    if ident in {b'RIFF', b'LIST', b'RF64', b'BW64', b'list'}:
        return parse_list_chunk(stream=stream, length=data_size,
                                rf64_context=rf64_context)

    else:
        data_start = stream.tell()
        stream.seek(displacement, 1)
        return ChunkDescriptor(ident=ident, start=data_start, length=data_size,
                               rf64_context=rf64_context)
