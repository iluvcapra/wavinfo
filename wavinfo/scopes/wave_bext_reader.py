from dataclasses import dataclass
import struct
# from .umid_parser import UMIDParser

from typing import Optional 

@dataclass
class Bext:
    """
    Broadcast-WAVE metadata fields.
    """
    #: BEXT version
    version: int
    
    #: Description. A free-text field up to 256 characters long.
    description: str

    #: Originator. Usually the name of the encoding application, sometimes an 
    #: artist name. 
    originator: str

    #: A unique identifier for the file, a serial number.
    originator_ref: str 

    #: Date of the recording, in the format YYYY-MM-DD.
    originator_date: str 
    
    #: Time of the recording, in the format HH:MM:SS.
    originator_time: str

    #: The sample offset of the start, usually relative to midnight.
    time_reference: int 

    #: A variable-length text field containing a list of processes and and 
    #: conversions performed on the file.
    coding_history: str
    
    #: SMPTE 330M UMID of this audio file, 64 bytes are allocated though the 
    #: UMID may only be 32 bytes long.
    umid: Optional[bytes]
    
    #: EBU R128 Integrated loudness, in LUFS.
    loudness_value: Optional[float]
    
    #: EBU R128 Loudness range, in LUFS.
    loudness_range: Optional[float]
    
    #: True peak level, in dBFS TP
    max_true_peak: Optional[float]
    
    #: EBU R128 Maximum momentary loudness, in LUFS
    max_momentary_loudness: Optional[float]
    
    #: EBU R128 Maximum short-term loudness, in LUFS.
    max_shortterm_loudness: Optional[float]

    def to_dict(self):
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

PACK_FORMAT = "<256s" + "32s" + "32s" + "10s" + "8s" + "QH" + "64s" + \
            "hhhhh" + "180s"

class WavBextReader:
    def __init__(self, encoding):
        """
        :param encoding: The encoding to use when decoding the text fields of
            the BEXT metadata scope. According to EBU Rec 3285 this shall be
            ASCII.
        """
        self.encoding = encoding
    
    def _sanitize_bytes(self, b: bytes) -> str:
            # honestly can't remember why I'm stripping nulls this way
            first_null = next((index for index, byte in enumerate(b)
                               if byte == 0), None)
            trimmed = b if first_null is None else b[:first_null]
            decoded = trimmed.decode(self.encoding)
            return decoded
    
    def read(self, bext_data) -> Bext:
        rest_starts = struct.calcsize(PACK_FORMAT)
        unpacked = struct.unpack(PACK_FORMAT, bext_data[:rest_starts])

        retval = Bext(description=self._sanitize_bytes(unpacked[0]),
                      originator=self._sanitize_bytes(unpacked[1]),
                      originator_ref=self._sanitize_bytes(unpacked[2]),
                      originator_date=self._sanitize_bytes(unpacked[3]),
                      originator_time=self._sanitize_bytes(unpacked[4]),
                      time_reference=unpacked[5],
                      coding_history=self._sanitize_bytes(bext_data[rest_starts:]),
                      version=unpacked[6], umid= None, loudness_value= None,
                      loudness_range= None, max_true_peak= None,
                      max_momentary_loudness= None, max_shortterm_loudness=
                      None)

        if retval.version > 0:
            retval.umid = unpacked[7]

        if retval.version > 1:
            retval.loudness_value = unpacked[8] / 100.0
            retval.loudness_range = unpacked[9] / 100.0
            retval.max_true_peak = unpacked[10] / 100.0
            retval.max_momentary_loudness = unpacked[11] / 100.0
            retval.max_shortterm_loudness = unpacked[12] / 100.0

        return retval


class WavBextWriter:
    encoding: str

    def __init__(self, encoding: str = 'ascii') -> None:
        self.encoding = encoding

    def _encode_string(self, s: str) -> bytes:
        retdata = s.encode(self.encoding)
        return retdata

    def write(self, bext: Bext) -> bytes:
        fields = [self._encode_string(bext.description),
                  self._encode_string(bext.originator),
                  self._encode_string(bext.originator_ref),
                  self._encode_string(bext.originator_date),
                  self._encode_string(bext.originator_time),
                  bext.time_reference,
                  bext.version,
                  ]

        if bext.version in (1, 2):
            fields.append(bext.umid)
        else:
            fields.append(b"\0")
        

        if bext.version == 2:
            assert bext.loudness_value
            assert bext.loudness_range
            assert bext.max_true_peak
            assert bext.max_momentary_loudness
            assert bext.max_shortterm_loudness
            fields.append(int(bext.loudness_value * 100))
            fields.append(int(bext.loudness_range * 100))
            fields.append(int(bext.max_true_peak * 100))
            fields.append(int(bext.max_momentary_loudness * 100))
            fields.append(int(bext.max_shortterm_loudness * 100))
        else:
            fields.extend([0, 0, 0, 0, 0])
        
        fields.append(b"\0")

        # breakpoint()
        leadin = struct.pack(PACK_FORMAT, *fields)

        return leadin + self._encode_string(bext.coding_history)

