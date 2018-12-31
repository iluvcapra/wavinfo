
import struct

from collections import namedtuple


ListChunkDescriptor = namedtuple('ListChunk' , 'signature children')


class ChunkDescriptor(namedtuple('Chunk', 'ident start length'):
    def read_data(from_stream):
        from_stream.seek(start)
        return from_stream.read(length)


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



WavInfoFormat = namedtuple("WavInfoFormat",'audio_format channel_count sample_rate byte_rate block_align bits_per_sample')

WavBextFormat = namedtuple("WavBextFormat",'description originator originator_ref ' + 
    'originator_date originator_time time_reference version umid loudness_value ' + 
    'loudness_range max_true_peak max_momentary_loudness max_shortterm_loudness coding_history')



class WavInfoReader( namedtuple("_WavInfoReaderImpl", "format bext ixml") ):
    """
    format : WAV format
    bext   : The Broadcast-WAV extension as definied by EBU Tech 3285 v2 (2011)

    """

    def __init__(self, path):
        with open(path, 'rb') as f:
            chunks = parse_chunk(f)
            
            f.seek(0)
            
            self.format = _get_format(chunks,f)
            self.info   = _get_bext(chunks,f)
            self.ixml   = _get_ixml(chunks,f)
        

    def _get_format(chunks,f):
        fmt_chunk = next(chunk for chunk in chunks if chunk.ident == b'fmt ')
        fmt_data = chunk.read_data(from_stream=f)
        
        # The format chunk is
        # audio_format    U16
        # channel_count   U16
        # sample_rate     U32   Note an integer
        # byte_rate       U32   == SampleRate * NumChannels * BitsPerSample/8
        # block_align     U16   == NumChannels * BitsPerSample/8
        # bits_per_sampl  U16
        unpacked = struct.unpack("<HHIIHH", fmt_data)

        return WavInfoFormat(audio_format = unpacked[0],
                channel_count = unpacked[1],
                sample_rate   = unpacked[2],
                byte_rate     = unpacked[3],
                block_align   = unpacked[4],
                bits_per_sample = unpacked[5]
                )

    def _get_bext(chunks,f):

        fmt_chunk = next(chunk for chunk in chunks if chunk.ident == b'bext')
        fmt_data = chunk.read_data(from_stream=f)

        # description[256]      
        # originator[32]
        # originatorref[32]
        # originatordate[10]   "YYYY:MM:DD"
        # originatortime[8]    "HH:MM:SS"
        # lowtimeref U32
        # hightimeref U32
        # version U16
        # umid[64]
        # loudnessvalue S16    (in LUFS*100)
        # loudnessrange S16    (in LUFS*100)
        # maxtruepeak   S16    (in dbTB*100)
        # maxmomentaryloudness S16 (LUFS*100)
        # maxshorttermloudness S16 (LUFS*100)
        # reserved[180]
        # codinghistory []

        packstring = "<256s"+ "32s" + "32s" + "10s" + "8s" + "QH" + "64s" + "hhhhh" + "180s"
        
        unpacked = struct.unpack(packstring, chunk)
        rest_starts = struct.calcsize(packstring)

        return WavBextFormat(description=unpacked[0],
                originator      = unpacked[1],
                originator_ref  = unpacked[2],
                originator_date = unpacked[3],
                originator_time = unpacked[4],
                time_reference  = unpacked[5],
                version         = unpacked[6],
                umid            = unpacked[7],
                loudness_value  = unpacked[8],
                loudness_range  = unpacked[9],
                max_true_peak   = unpacked[10],
                max_momentary_loudness = unpacked[11],
                max_shortterm_loudness = unpacked[12],
                coding_history = fmt_data[rest_starts:]
                )


        





        




