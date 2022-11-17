import struct
from .umid_parser import UMIDParser

from typing import Optional

class WavBextReader:
    def __init__(self, bext_data, encoding):
        """
        Read Broadcast-WAV extended metadata.
        :param bext_data: The bytes-like data.
        :param encoding: The encoding to use when decoding the text fields of the
                 BEXT metadata scope. According to EBU Rec 3285 this shall be ASCII.
        """
        packstring = "<256s" + "32s" + "32s" + "10s" + "8s" + "QH" + "64s" + "hhhhh" + "180s"

        rest_starts = struct.calcsize(packstring)
        unpacked = struct.unpack(packstring, bext_data[:rest_starts])

        def sanitize_bytes(b : bytes) -> str:
            first_null = next((index for index, byte in enumerate(b) if byte == 0), None)
            trimmed = b if first_null is None else b[:first_null]
            decoded = trimmed.decode(encoding)
            return decoded

        #: Description. A free-text field up to 256 characters long.
        self.description : str = sanitize_bytes(unpacked[0])
        #: Originator. Usually the name of the encoding application, sometimes
        #: a artist name.
        self.originator : str = sanitize_bytes(unpacked[1])
        #: A unique identifier for the file, a serial number.
        self.originator_ref : str = sanitize_bytes(unpacked[2])
        #: Date of the recording, in the format YYY-MM-DD
        self.originator_date : str = sanitize_bytes(unpacked[3])
        #: Time of the recording, in the format HH:MM:SS.
        self.originator_time : str = sanitize_bytes(unpacked[4])
        #: The sample offset of the start of the file relative to an
        #: epoch, usually midnight the day of the recording. 
        self.time_reference : int  = unpacked[5]
        #: A variable-length text field containing a list of processes and
        #: and conversions performed on the file.
        self.coding_history : str = sanitize_bytes(bext_data[rest_starts:])
        #: BEXT version. 
        self.version : int = unpacked[6]
        #: SMPTE 330M UMID of this audio file, 64 bytes are allocated though the UMID
        #: may only be 32 bytes long.
        self.umid : Optional[bytes] = None
        #: EBU R128 Integrated loudness, in LUFS.
        self.loudness_value : Optional[float] = None
        #: EBU R128 Loudness rante, in LUFS.
        self.loudness_range : Optional[float] = None
        #: True peak level, in dBFS TP
        self.max_true_peak : Optional[float] = None
        #: EBU R128 Maximum momentary loudness, in LUFS
        self.max_momentary_loudness : Optional[float] = None
        #: EBU R128 Maximum short-term loudness, in LUFS.
        self.max_shortterm_loudness : Optional[float] = None

        if self.version > 0:
            self.umid = unpacked[7]

        if self.version > 1:
            self.loudness_value = unpacked[8] / 100.0
            self.loudness_range = unpacked[9] / 100.0
            self.max_true_peak = unpacked[10] / 100.0
            self.max_momentary_loudness = unpacked[11] / 100.0
            self.max_shortterm_loudness = unpacked[12] / 100.0

    def to_dict(self):
        if self.umid is not None:
            umid_parsed = UMIDParser(self.umid)
            umid_str = umid_parsed.basic_umid_to_str()
        else:
            umid_str = None

        return {'description': self.description,
                'originator': self.originator,
                'originator_ref': self.originator_ref,
                'originator_date': self.originator_date,
                'originator_time': self.originator_time,
                'time_reference': self.time_reference,
                'version': self.version,
                'umid': umid_str,
                'coding_history': self.coding_history,
                'loudness_value': self.loudness_value,
                'loudness_range': self.loudness_range,
                'max_true_peak': self.max_true_peak,
                'max_momentary_loudness': self.max_momentary_loudness,
                'max_shortterm_loudness': self.max_shortterm_loudness
                }
