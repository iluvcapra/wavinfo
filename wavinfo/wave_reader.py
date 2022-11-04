#-*- coding: utf-8 -*-
import struct
import os
from collections import namedtuple

import pathlib

from .riff_parser import parse_chunk, ChunkDescriptor, ListChunkDescriptor
from .wave_ixml_reader import WavIXMLFormat
from .wave_bext_reader import WavBextReader
from .wave_info_reader import WavInfoChunkReader

#: Calculated statistics about the audio data.
WavDataDescriptor = namedtuple('WavDataDescriptor', 'byte_count frame_count')

#: The format of the audio samples.
WavAudioFormat = namedtuple('WavAudioFormat',
                            'audio_format channel_count sample_rate byte_rate block_align bits_per_sample')


class WavInfoReader:
    """
    Parse a WAV audio file for metadata.
    """

    def __init__(self, path, info_encoding='latin_1', bext_encoding='ascii'):
        """
        Create a new reader object.

        :param path: 
            A filesystem path to the wav file you wish to probe or a 
            file handle to an open file.

        :param info_encoding: 
            The text encoding of the INFO metadata fields.
            latin_1/Win CP1252 has always been a pretty good guess for this.

        :param bext_encoding: 
            The text encoding to use when decoding the string
            fields of the Broadcast-WAV extension. Per EBU 3285 this is ASCII
            but this parameter is available to you if you encounter a weirdo.
        """
        
        self.info_encoding = info_encoding
        self.bext_encoding = bext_encoding
        
        if hasattr(path, 'read'):
            self.get_wav_info(path)
            self.url = 'about:blank'
            self.path = repr(path)
        else:
            absolute_path = os.path.abspath(path)

            #: `file://` url for the file.
            self.url = pathlib.Path(absolute_path).as_uri()

            # for __repr__()
            self.path = absolute_path
            
            with open(path, 'rb') as f:
                self.get_wav_info(f)
            
    def get_wav_info(self, wavfile):
        chunks = parse_chunk(wavfile)

        self.main_list = chunks.children
        wavfile.seek(0)

        #: :class:`wavinfo.wave_reader.WavAudioFormat`
        self.fmt = self._get_format(wavfile)

        #: :class:`wavinfo.wave_bext_reader.WavBextReader` with Broadcast-WAV metadata
        self.bext = self._get_bext(wavfile, encoding=self.bext_encoding)

        #: :class:`wavinfo.wave_ixml_reader.WavIXMLFormat` with iXML metadata
        self.ixml = self._get_ixml(wavfile)

        #: :class:`wavinfo.wave_info_reader.WavInfoChunkReader` with RIFF INFO metadata
        self.info = self._get_info(wavfile, encoding=self.info_encoding)
        self.data = self._describe_data()

    def _find_chunk_data(self, ident, from_stream, default_none=False):
        top_chunks = (chunk for chunk in self.main_list if type(chunk) is ChunkDescriptor and chunk.ident == ident)
        chunk_descriptor = next(top_chunks, None) if default_none else next(top_chunks)
        return chunk_descriptor.read_data(from_stream) if chunk_descriptor else None

    def _describe_data(self):
        data_chunk = next(c for c in self.main_list if c.ident == b'data')

        return WavDataDescriptor(byte_count=data_chunk.length,
                                 frame_count=int(data_chunk.length / self.fmt.block_align))

    def _get_format(self, f):
        fmt_data = self._find_chunk_data(b'fmt ', f)

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

        # 0x0001	WAVE_FORMAT_PCM	PCM
        # 0x0003	WAVE_FORMAT_IEEE_FLOAT	IEEE float
        # 0x0006	WAVE_FORMAT_ALAW	8-bit ITU-T G.711 A-law
        # 0x0007	WAVE_FORMAT_MULAW	8-bit ITU-T G.711 µ-law
        # 0xFFFE	WAVE_FORMAT_EXTENSIBLE	Determined by SubFormat

        # https://sno.phy.queensu.ca/~phil/exiftool/TagNames/RIFF.html
        return WavAudioFormat(audio_format=unpacked[0],
                              channel_count=unpacked[1],
                              sample_rate=unpacked[2],
                              byte_rate=unpacked[3],
                              block_align=unpacked[4],
                              bits_per_sample=unpacked[5]
                              )

    def _get_info(self, f, encoding):
        finder = (chunk.signature for chunk in self.main_list if type(chunk) is ListChunkDescriptor)

        if b'INFO' in finder:
            return WavInfoChunkReader(f, encoding)

    def _get_bext(self, f, encoding):
        bext_data = self._find_chunk_data(b'bext', f, default_none=True)
        return WavBextReader(bext_data, encoding) if bext_data else None

    def _get_ixml(self, f):
        ixml_data = self._find_chunk_data(b'iXML', f, default_none=True)
        return None if ixml_data is None else WavIXMLFormat(ixml_data.rstrip(b'\0'))

    def walk(self):
        """
        Walk all of the available metadata fields.

        :yields: a string, the :scope: of the metadatum, the string :name: of the
        metadata field, and the value.
        """

        scopes = ('fmt', 'data')  # 'bext', 'ixml', 'info')

        for scope in scopes:
            attr = self.__getattribute__(scope)
            for field in attr._fields:
                yield scope, field, attr.__getattribute__(field)

            if self.bext is not None:
                bext_dict = (self.bext or {}).to_dict()
                for key in bext_dict.keys():
                    yield 'bext', key, bext_dict[key]

            if self.info is not None:
                info_dict = self.info.to_dict()
                for key in info_dict.keys():
                    yield 'info', key, info_dict[key]

    def __repr__(self):
        return 'WavInfoReader({}, {}, {})'.format(self.path, self.info_encoding, self.bext_encoding)
