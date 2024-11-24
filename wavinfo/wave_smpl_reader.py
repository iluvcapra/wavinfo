import struct

from enum import IntEnum
from typing import Tuple, NamedTuple, List


class WaveSmplLoop(NamedTuple):
    ident: int 
    loop_type: int 
    start: int 
    end: int
    fraction: int
    repetition_count: int


class WaveSmplReader:
    
    def __init__(self, smpl_data: bytes):
        """
        Read sampler metadata from smpl chunk.
        """
        
        header_field_fmt = "<IIIIIIbbbbII"
        loop_field_fmt = "<IIIIII"
        header_size = struct.calcsize(header_field_fmt)
        loop_size = struct.calcsize(loop_field_fmt)

        unpacked_data = struct.unpack(header_field_fmt, 
                                      smpl_data[0:header_size])

        #: The MIDI Manufacturer's Association code for the sampler manufactuer,
        #: or 0 if not specific.
        self.manufacturer: int = unpacked_data[0]

        #: The manufacturer-assigned code for their specific sampler model, or
        #: 0 if not specific.
        self.product: int = unpacked_data[1]

        #: The number of nanoseconds in one audio frame.
        self.sample_period: int = unpacked_data[2]

        #: The MIDI note number for the loops in this sample 
        self.midi_note: int = unpacked_data[3]

        #: The number of semitones above the MIDI note the loops tune for.
        self.midi_pitch_fraction: int = unpacked_data[4]

        #: SMPTE timecode format, one of (0, 24, 25, 29, 30)
        self.smpte_format: int = unpacked_data[5]

        #: The SMPTE offset to apply, as a tuple of four ints representing 
        #: hh, mm, ss, ff
        self.smpte_offset: Tuple[int, int, int, int]  = unpacked_data[6:10]
        
        loop_count = unpacked_data[10]
        sampler_udata_length = unpacked_data[11]

        #: List of loops in the file.
        self.sample_loops: List[WaveSmplLoop] = [] 
        
        loop_buffer = smpl_data[header_field_fmt:
                                header_field_fmt + loop_size * loop_count]

        for unpacked_loop in struct.iter_unpack(loop_field_fmt, loop_buffer):
            self.sample_loops.append(WaveSmplLoop(
                ident=unpacked_loop[0], 
                loop_type=unpacked_loop[1],
                start=unpacked_loop[2],
                end=unpacked_loop[3],
                fraction=unpacked_loop[4],
                repetition_count=unpacked_loop[5]))

        #: Sampler-specific user data.
        self.sampler_udata: bytes = smpl_data[
                header_field_fmt + loop_size * loop_count : 
                header_field_fmt + loop_size * loop_count + sampler_udata_length]


