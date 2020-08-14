import struct
from collections import namedtuple
from . import riff_parser

RF64Context = namedtuple('RF64Context','sample_count bigchunk_table')


def parse_rf64(stream, signature = b'RF64'):
    # print("starting parse_rf64")
    start = stream.tell()
    assert( stream.read(4) == b'WAVE' )

    ds64_chunk = riff_parser.parse_chunk(stream)

    ds64_field_spec = "<QQQI"
    ds64_fields_size = struct.calcsize(ds64_field_spec)
    assert(ds64_chunk.ident == b'ds64')

    ds64_data = ds64_chunk.read_data(stream)
    assert(len(ds64_data) >= ds64_fields_size )

    # print("Read ds64 chunk: len()",len(ds64_data))
    riff_size, data_size, sample_count, length_lookup_table = struct.unpack( ds64_field_spec , ds64_data[0:ds64_fields_size] )

    bigchunk_table = {}
    chunksize64format = "<4sL"
    chunksize64size = struct.calcsize(chunksize64format)
    # print("Found chunks64s:", length_lookup_table)

    for n in range(length_lookup_table):
        bigname, bigsize = struct.unpack_from( chunksize64format , ds64_data, offset= ds64_fields_size )
        bigchunk_table[bigname] = bigsize

    bigchunk_table[b'data'] = data_size
    bigchunk_table[signature] = riff_size

    stream.seek(start, 0)
    # print("returning from parse_rf64, context: ", RF64Context(sample_count=sample_count, bigchunk_table=bigchunk_table))
    return RF64Context( sample_count=sample_count, bigchunk_table=bigchunk_table )

