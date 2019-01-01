import struct

from collections import namedtuple

from .wave_parser import parse_chunk, ChunkDescriptor, ListChunkDescriptor
from .wave_ixml_reader import WavIXMLFormat

WavDataDescriptor = namedtuple('WavDataDescriptor','byte_count frame_count')

WavInfoFormat = namedtuple("WavInfoFormat",'audio_format channel_count sample_rate byte_rate block_align bits_per_sample')

WavBextFormat = namedtuple("WavBextFormat",'description originator originator_ref ' +
    'originator_date originator_time time_reference version umid ' +
    'loudness_value loudness_range max_true_peak max_momentary_loudness max_shortterm_loudness ' +
    'coding_history')


class WavInfoReader():
    """
    format : WAV format
    bext   : The Broadcast-WAV extension as definied by EBU Tech 3285 v2 (2011)

    """

    def __init__(self, path):
        with open(path, 'rb') as f:
            chunks = parse_chunk(f)

            self.main_list = chunks.children
            f.seek(0)

            self.fmt    = self._get_format(f)
            self.bext   = self._get_bext(f)
            self.ixml   = self._get_ixml(f)

            self.data   = self._describe_data(f)

    def _find_chunk_data(self, ident, from_stream, default_none=False):
        chunk_descriptor = None
        top_chunks = (chunk for chunk in self.main_list if type(chunk) is ChunkDescriptor)

        if default_none:
            chunk_descriptor = next((chunk for chunk in top_chunks if chunk.ident == ident),None)
        else:
            chunk_descriptor = next((chunk for chunk in top_chunks if chunk.ident == ident))

        if chunk_descriptor:
            return chunk_descriptor.read_data(from_stream)
        else:
            return None


    def _describe_data(self,f):
        data_chunk = next(c for c in self.main_list if c.ident == b'data')

        return WavDataDescriptor(byte_count= data_chunk.length,
                frame_count= int(data_chunk.length / self.fmt.block_align))



    def _get_format(self,f):
        fmt_data = self._find_chunk_data(b'fmt ',f)

        # The format chunk is
        # audio_format    U16
        # channel_count   U16
        # sample_rate     U32   Note an integer
        # byte_rate       U32   == SampleRate * NumChannels * BitsPerSample/8
        # block_align     U16   == NumChannels * BitsPerSample/8
        # bits_per_sampl  U16
        packstring = "<HHIIHH"
        rest_starts = struct.calcsize(packstring)

        unpacked = struct.unpack(packstring, fmt_data[:rest_starts])

        #0x0001	WAVE_FORMAT_PCM	PCM
        #0x0003	WAVE_FORMAT_IEEE_FLOAT	IEEE float
        #0x0006	WAVE_FORMAT_ALAW	8-bit ITU-T G.711 A-law
        #0x0007	WAVE_FORMAT_MULAW	8-bit ITU-T G.711 µ-law
        #0xFFFE	WAVE_FORMAT_EXTENSIBLE	Determined by SubFormat
        if unpacked[0] == 0x0001:
            return WavInfoFormat(audio_format = unpacked[0],
                    channel_count = unpacked[1],
                    sample_rate   = unpacked[2],
                    byte_rate     = unpacked[3],
                    block_align   = unpacked[4],
                    bits_per_sample = unpacked[5]
                    )

    def _get_bext(self,f):

        bext_data = self._find_chunk_data(b'bext',f,default_none=True)

        # description[256]
        # originator[32]
        # originatorref[32]
        # originatordate[10]   "YYYY:MM:DD"
        # originatortime[8]    "HH:MM:SS"
        # lowtimeref U32
        # hightimeref U32
        # version U16
        # umid[64]
        #
        # EBU 3285 fields
        # loudnessvalue S16    (in LUFS*100)
        # loudnessrange S16    (in LUFS*100)
        # maxtruepeak   S16    (in dbTB*100)
        # maxmomentaryloudness S16 (LUFS*100)
        # maxshorttermloudness S16 (LUFS*100)
        # reserved[180]
        # codinghistory []
        if bext_data is None:
            return None

        packstring = "<256s"+ "32s" + "32s" + "10s" + "8s" + "QH" + "64s" + "hhhhh" + "180s"

        rest_starts = struct.calcsize(packstring)
        unpacked = struct.unpack(packstring, bext_data[:rest_starts])

        return WavBextFormat(description=unpacked[0].decode('ascii').rstrip('\0'),
                originator      = unpacked[1].decode('ascii').rstrip('\0'),
                originator_ref  = unpacked[2].decode('ascii').rstrip('\0'),
                originator_date = unpacked[3].decode('ascii'),
                originator_time = unpacked[4].decode('ascii'),
                time_reference  = unpacked[5],
                version         = unpacked[6],
                umid            = unpacked[7],
                loudness_value  = unpacked[8] / 100.0,
                loudness_range  = unpacked[9] / 100.0,
                max_true_peak   = unpacked[10] / 100.0,
                max_momentary_loudness = unpacked[11] / 100.0,
                max_shortterm_loudness = unpacked[12] / 100.0,
                coding_history = bext_data[rest_starts:].decode('ascii').rstrip('\0')
                )

    def _get_ixml(self,f):

        ixml_data = self._find_chunk_data(b'iXML',f,default_none=True)
        if ixml_data is None:
            return None

        ixml_string = ixml_data.decode('utf-8')
        return WavIXMLFormat(ixml_string)





