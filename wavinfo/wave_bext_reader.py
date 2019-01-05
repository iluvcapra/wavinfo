import struct

class WavBextReader:
    def __init__(self,bext_data,encoding):
        # description[256]

        # originator[32]
        # originatorref[32]
        # originatordate[10]   "YYYY:MM:DD"
        # originatortime[8]    "HH:MM:SS"
        # lowtimeref U32
        # hightimeref U32
        # version U16
        #
        # V1 field
        # umid[64]
        #
        # V2 fields
        # loudnessvalue S16    (in LUFS*100)
        # loudnessrange S16    (in LUFS*100)
        # maxtruepeak   S16    (in dbTB*100)
        # maxmomentaryloudness S16 (LUFS*100)
        # maxshorttermloudness S16 (LUFS*100)
        #
        # reserved[180]
        # codinghistory []
        packstring = "<256s"+ "32s" + "32s" + "10s" + "8s" + "QH" + "64s" + "hhhhh" + "180s"

        rest_starts = struct.calcsize(packstring)
        unpacked = struct.unpack(packstring, bext_data[:rest_starts])

        def sanatize_bytes(bytes):
            first_null = next( (index for index, byte in enumerate(bytes) if byte == 0 ), None )
            if first_null is not None:
                trimmed = bytes[:first_null]
            else:
                trimmed = bytes

            decoded = trimmed.decode(encoding)
            return decoded

        self.description     = sanatize_bytes(unpacked[0])
        self.originator      = sanatize_bytes(unpacked[1])
        self.originator_ref  = sanatize_bytes(unpacked[2])
        self.originator_date = sanatize_bytes(unpacked[3])
        self.originator_time = sanatize_bytes(unpacked[4])
        self.time_reference  = unpacked[5]
        self.version         = unpacked[6]
        self.umid            = None
        self.loudness_value          = None
        self.loudness_range          = None
        self.max_true_peak           = None
        self.max_momentary_loudness  = None
        self.max_shortterm_loudness  = None
        self.coding_history  = sanatize_bytes(bext_data[rest_starts:])

        if self.version > 0:
            self.umid = unpacked[7]

        if self.version > 1:
            self.loudness_value          = unpacked[8] / 100.0
            self.loudness_range          = unpacked[9] / 100.0
            self.max_true_peak           = unpacked[10] / 100.0
            self.max_momentary_loudness  = unpacked[11] / 100.0
            self.max_shortterm_loudness  = unpacked[12] / 100.0


    def to_dict(self):
        return {'description':      self.description,
                'originator':       self.originator,
                'originator_ref':   self.originator_ref,
                'originator_date':  self.originator_date,
                'originator_time':  self.originator_time,
                'time_reference':   self.time_reference,
                'version':          self.version,
                'coding_history':   self.coding_history,
                'loudness_value':   self.loudness_value,
                'loudness_range':   self.loudness_range,
                'max_true_peak':    self.max_true_peak,
                'max_momentary_loudness':   self.max_momentary_loudness,
                'max_shortterm_loudness':   self.max_shortterm_loudness
                }

