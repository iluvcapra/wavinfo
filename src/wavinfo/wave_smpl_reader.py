import struct

from typing import Tuple, NamedTuple, List


class WaveSmplLoop(NamedTuple):
    ident: int
    loop_type: int
    start: int
    end: int
    detune_cents: int
    repetition_count: int

    def loop_type_desc(self):
        if self.loop_type == 0:
            return 'FORWARD'
        elif self.loop_type == 1:
            return 'FORWARD_BACKWARD'
        elif self.loop_type == 2:
            return 'BACKWARD'
        elif 3 <= self.loop_type <= 31:
            return 'RESERVED'
        else:
            return 'VENDOR'

    def to_dict(self):
        return {
            'ident': self.ident,
            'loop_type': self.loop_type,
            'loop_type_description': self.loop_type_desc(),
            'start_samples': self.start,
            'end_samples': self.end,
            'detune_cents': self.detune_cents,
            'repetition_count': self.repetition_count,
        }


class WavSmplReader:

    def __init__(self, smpl_data: bytes):
        """
        Read sampler metadata from smpl chunk.
        """

        header_field_fmt = "<IIIIiIbbbbII"
        loop_field_fmt = "<IIIIiI"
        header_size = struct.calcsize(header_field_fmt)
        loop_size = struct.calcsize(loop_field_fmt)

        unpacked_data = struct.unpack(header_field_fmt,
                                      smpl_data[0:header_size])

        #: The MIDI Manufacturer's Association code for the sampler
        #: manufactuer, or 0 if not specific.
        self.manufacturer: int = unpacked_data[0]

        #: The manufacturer-assigned code for their specific sampler model, or
        #: 0 if not specific.
        self.product: int = unpacked_data[1]

        #: The number of nanoseconds in one audio frame.
        self.sample_period_ns: int = unpacked_data[2]

        #: The MIDI note number for the loops in this sample
        self.midi_note: int = unpacked_data[3]

        #: The number of semitones above the MIDI note the loops tune for.
        self.midi_pitch_detune_cents: int = unpacked_data[4]

        #: SMPTE timecode format, one of (0, 24, 25, 29, 30)
        self.smpte_format: int = unpacked_data[5]

        #: The SMPTE offset to apply, as a tuple of four ints representing
        #: hh, mm, ss, ff
        self.smpte_offset: Tuple[int, int, int, int] = unpacked_data[6:10]

        loop_count = unpacked_data[10]
        sampler_udata_length = unpacked_data[11]

        #: List of loops in the file.
        self.sample_loops: List[WaveSmplLoop] = []

        loop_buffer = smpl_data[header_size:
                                header_size + loop_size * loop_count]

        for unpacked_loop in struct.iter_unpack(loop_field_fmt, loop_buffer):
            self.sample_loops.append(WaveSmplLoop(
                ident=unpacked_loop[0],
                loop_type=unpacked_loop[1],
                start=unpacked_loop[2],
                end=unpacked_loop[3],
                detune_cents=unpacked_loop[4],
                repetition_count=unpacked_loop[5]))

        #: Sampler-specific user data.
        self.sampler_udata: bytes | None = None

        if sampler_udata_length > 0:
            self.sampler_udata = smpl_data[
                header_size + loop_size * loop_count:
                header_size + loop_size * loop_count + sampler_udata_length]

    def to_dict(self):
        return {
            'manufactuer': self.manufacturer,
            'product': self.product,
            'sample_period_ns': self.sample_period_ns,
            'midi_note': self.midi_note,
            'midi_pitch_detune_cents': self.midi_pitch_detune_cents,
            'smpte_format': self.smpte_format,
            'smpte_offset': "%02i:%02i:%02i:%02i" % self.smpte_offset,
            'loops': [x.to_dict() for x in self.sample_loops],
            'sampler_user_data': self.sampler_udata,
        }
