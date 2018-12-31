import struct

class WavInfoReader():
    """
    format : WAV format
    bext   : The Broadcast-WAV extension as definied by EBU Tech 3285 v2 (2011)

    """

    def __init__(self, path):
        with open(path, 'rb') as f:
            chunks = parse_chunk(f)
            
            main_list = chunks.children
            f.seek(0)
            
            self.fmt    = self._get_format(main_list,f)
            self.info   = self._get_bext(main_list,f)
            self.ixml   = self._get_ixml(main_list,f)


    def _get_format(self,chunks,f):
        fmt_chunk = next(chunk for chunk in chunks if chunk.ident == b'fmt ')
        fmt_data = fmt_chunk.read_data(f)
        
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

    def _get_bext(self,chunks,f):

        bext_chunk = next((chunk for chunk in chunks if chunk.ident == b'bext'),None)
        bext_data = bext_chunk.read_data(from_stream=f)

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
        print(len(bext_data))
        packstring = "<256s"+ "32s" + "32s" + "10s" + "8s" + "QH" + "64s" + "hhhhh" + "180s"
        
        rest_starts = struct.calcsize(packstring)
        unpacked = struct.unpack(packstring, bext_data[:rest_starts])
        

        return WavBextFormat(description=unpacked[0].decode('ascii').rstrip(' \t\r\n\0'),
                originator      = unpacked[1].decode('ascii').rstrip(' \t\r\n\0'),
                originator_ref  = unpacked[2].decode('ascii').rstrip(' \t\r\n\0'),
                originator_date = unpacked[3].decode('ascii').rstrip(' \t\r\n\0'),
                originator_time = unpacked[4].decode('ascii').rstrip(' \t\r\n\0'),
                time_reference  = unpacked[5],
                version         = unpacked[6],
                umid            = unpacked[7],
                loudness_value  = unpacked[8],
                loudness_range  = unpacked[9],
                max_true_peak   = unpacked[10],
                max_momentary_loudness = unpacked[11],
                max_shortterm_loudness = unpacked[12],
                coding_history = bext_data[rest_starts:].decode('ascii').rstrip(' \t\r\n\0')
                )

    def _get_ixml(self,chunks,f):

        ixml_chunk = next((chunk for chunk in chunks if chunk.ident == b'iXML'),None)
        ixml_data = ixml_chunk.read_data(from_stream=f)
        ixml_string = ixml_data.decode('utf-8')

        return WavIXMLFormat(ixml_string)
        


        

