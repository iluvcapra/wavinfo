#-*- coding: utf-8 -*-
import struct
import os
from collections import namedtuple

from typing import Optional, Generator, Any

import pathlib

from .riff_parser import parse_chunk, ChunkDescriptor, ListChunkDescriptor
from .wave_ixml_reader import WavIXMLFormat
from .wave_bext_reader import WavBextReader
from .wave_info_reader import WavInfoChunkReader
from .wave_adm_reader import WavADMReader
from .wave_dbmd_reader import WavDolbyMetadataReader
from .wave_cues_reader import WavCuesReader

#: Calculated statistics about the audio data.
WavDataDescriptor = namedtuple('WavDataDescriptor', 'byte_count frame_count')

#: The format of the audio samples.
WavAudioFormat = namedtuple('WavAudioFormat',
                            ['audio_format', 'channel_count', 'sample_rate',
                             'byte_rate',  'block_align',  'bits_per_sample'])


class WavInfoReader:
    """
    Parse a WAV audio file for metadata.
    """

    def __init__(self, path, info_encoding='latin_1', bext_encoding='ascii'):
        """
        Create a new reader object.

        :param path: 
            A pathlike object or IO to the wav file you wish to probe or a 
            file handle to an open file.

        :param info_encoding: 
            The text encoding of the ``INFO``, ``LABL`` and other RIFF-defined
            metadata fields. 

        :param bext_encoding: 
            The text encoding to use when decoding the string
            fields of the Broadcast-WAV extension. Per EBU 3285 this is ASCII
            but this parameter is available to you if you encounter a weirdo.
        """
        
        self.info_encoding = info_encoding
        self.bext_encoding = bext_encoding
        
        #: Wave audio data format.
        self.fmt :Optional[WavAudioFormat] = None

        #: Statistics of the `data` section.
        self.data :Optional[WavDataDescriptor] = None

        #: Broadcast-Wave metadata.
        self.bext :Optional[WavBextReader] = None

        #: iXML metadata.
        self.ixml :Optional[WavIXMLFormat] = None

        #: ADM Audio Definiton Model metadata.
        self.adm :Optional[WavADMReader]= None

        #: Dolby bitstream metadata.
        self.dolby :Optional[WavDolbyMetadataReader] = None

        #: RIFF INFO metadata.
        self.info :Optional[WavInfoChunkReader]= None

        #: RIFF cues markers, labels, and notes.
        self.cues :Optional[WavCuesReader] = None

        if hasattr(path, 'read'):
            self.get_wav_info(path)
            self.url = 'about:blank'
            self.path = repr(path)
            
        else:
            absolute_path = os.path.abspath(path)

            #: `file://` url for the file.
            self.url: str = pathlib.Path(absolute_path).as_uri()

            self.path = absolute_path
        
            with open(path, 'rb') as f:
                self.get_wav_info(f)
            
    def get_wav_info(self, wavfile):
        chunks = parse_chunk(wavfile)
        assert type(chunks) is ListChunkDescriptor  

        self.main_list = chunks.children
        wavfile.seek(0)

        self.fmt = self._get_format(wavfile)
        self.bext = self._get_bext(wavfile, encoding=self.bext_encoding)
        self.ixml = self._get_ixml(wavfile)
        self.adm  = self._get_adm(wavfile)
        self.info = self._get_info(wavfile, encoding=self.info_encoding)
        self.dolby = self._get_dbmd(wavfile)
        self.cues = self._get_cue(wavfile)
        self.data = self._describe_data()

    def _find_chunk_data(self, ident, from_stream, default_none=False) -> Optional[bytes]:
        top_chunks = (chunk for chunk in self.main_list \
            if type(chunk) is ChunkDescriptor and chunk.ident == ident)

        chunk_descriptor = next(top_chunks, None) \
            if default_none else next(top_chunks)

        return chunk_descriptor.read_data(from_stream) \
            if chunk_descriptor else None

    def _find_list_chunk(self, signature) -> Optional[ListChunkDescriptor]:
        top_chunks = (chunk for chunk in self.main_list \
            if type(chunk) is ListChunkDescriptor and \
                chunk.signature == signature)

        return next(top_chunks, None)

    def _describe_data(self):
        data_chunk = next(c for c in self.main_list \
            if type(c) is ChunkDescriptor and c.ident == b'data')

        assert isinstance(self.fmt, WavAudioFormat)
        return WavDataDescriptor(
            byte_count=data_chunk.length, 
            frame_count=int(data_chunk.length / self.fmt.block_align))

    def _get_format(self, f):
        fmt_data = self._find_chunk_data(b'fmt ', f)
        assert fmt_data is not None, "Fmt data not found, not a valid wav file"

        packstring = "<HHIIHH"
        rest_starts = struct.calcsize(packstring)

        unpacked = struct.unpack(packstring, fmt_data[:rest_starts])

        return WavAudioFormat(audio_format=unpacked[0],
                              channel_count=unpacked[1],
                              sample_rate=unpacked[2],
                              byte_rate=unpacked[3],
                              block_align=unpacked[4],
                              bits_per_sample=unpacked[5]
                              )

    def _get_info(self, f, encoding):
        finder = (chunk.signature for chunk in self.main_list \
            if type(chunk) is ListChunkDescriptor)

        if b'INFO' in finder:
            return WavInfoChunkReader(f, encoding)

    def _get_bext(self, f, encoding):
        bext_data = self._find_chunk_data(b'bext', f, default_none=True)
        return WavBextReader(bext_data, encoding) if bext_data else None

    def _get_adm(self, f):
        axml = self._find_chunk_data(b'axml', f, default_none=True)
        chna = self._find_chunk_data(b'chna', f, default_none=True)
        return WavADMReader(axml_data=axml, chna_data=chna) \
            if axml and chna else None

    def _get_dbmd(self, f):
        dbmd_data = self._find_chunk_data(b'dbmd', f, default_none=True)
        return WavDolbyMetadataReader(dbmd_data=dbmd_data) \
            if dbmd_data else None

    def _get_ixml(self, f):
        ixml_data = self._find_chunk_data(b'iXML', f, default_none=True)
        return WavIXMLFormat(ixml_data.rstrip(b'\0')) if ixml_data else None

    def _get_cue(self, f):
        cue = next((cue_chunk for cue_chunk in self.main_list if \
            type(cue_chunk) is ChunkDescriptor and \
            cue_chunk.ident == b'cue '), None)

        adtl = self._find_list_chunk(b'adtl')
        labls = []
        ltxts = []
        notes = []
        if adtl is not None:
            labls = [c for c in adtl.children if c.ident == b'labl']
            ltxts = [c for c in adtl.children if c.ident == b'ltxt']
            notes = [c for c in adtl.children if c.ident == b'note']

        return WavCuesReader.read_all(f, cue, labls, ltxts, notes, 
                                   fallback_encoding=self.info_encoding)

    def walk(self) -> Generator[str,str,Any]: #FIXME: this should probably be named "iter()"
        """
        Walk all of the available metadata fields.
        
        :yields: tuples of the *scope*, *key*, and *value* of
            each metadatum. The *scope* value will be one of
            "fmt", "data", "ixml", "bext", "info", "dolby", "cues" or "adm".
        """

        scopes = ('fmt', 'data', 'ixml', 'bext', 'info', 'adm', 'cues', 
                 'dolby')

        for scope in scopes:
            if scope in ['fmt', 'data']:
                attr = self.__getattribute__(scope)
                for field in attr._fields:
                    yield scope, field, attr.__getattribute__(field)

            else:
                dict = self.__getattribute__(scope).to_dict() if self.__getattribute__(scope) else {}
                for key in dict.keys():
                    yield scope, key, dict[key]
        
    def __repr__(self):
        return 'WavInfoReader({}, {}, {})'.format(self.path, self.info_encoding, self.bext_encoding)
