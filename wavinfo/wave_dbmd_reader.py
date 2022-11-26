"""
Reading Dolby Bitstream Metadata

Unless otherwise stated, all § references here are to 
`EBU Tech 3285 Supplement 6`_.

.. _EBU Tech 3285 Supplement 6: https://tech.ebu.ch/docs/tech/tech3285s6.pdf
"""

from enum import IntEnum, Enum
from struct import unpack
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple, Any, Union

from io import BytesIO

class SegmentType(IntEnum):
    """
    Metadata segment type.
    """
    EndMarker = 0x0
    DolbyE = 0x1
    # Reserved2 = 0x2
    DolbyDigital = 0x3
    # Reserved4 = 0x4
    # Reserved5 = 0x5
    # Reserved6 = 0x6
    DolbyDigitalPlus = 0x7
    AudioInfo = 0x8
    DolbyAtmos = 0x9
    DolbyAtmosSupplemental = 0xa

    @classmethod
    def _missing_(cls,val):
        return val


@dataclass
class DolbyDigitalPlusMetadata:
    """
    *Dolby Digital Plus* is Dolby's brand for multichannel surround
    on discrete formats that aren't AC-3 (Dolby Digital) or Dolby E. This 
    metadata segment is present in ADM wave files created with a Dolby Atmos 
    Production Suite.

    Where an AC-3 bitstream can contain multiple programs, a Dolby Digital 
    Plus bitstream will only contain one program.
    """

    class DownMixLevelToken(Enum):
        """
        A gain coefficient used in several metadata fields for downmix
        scenarios.
        """

        PLUS_3DB = 0b000
        "+3 dB"

        PLUS_1_5DB = 0b001
        "+1.5 dB"

        UNITY = 0b010
        "0dB"

        MINUS_1_5DB = 0b011
        "-1.5 dB"

        MINUS_3DB = 0b100
        "-3 dB"

        MINUS_4_5DB = 0b101
        "-4.5 dB"

        MINUS_6DB = 0b110
        "-6 dB"

        MUTE = 0b111
        "-∞ dB"


    class DolbySurroundEncodingMode(Enum):
        """
        Dolby surround endcoding mode.
        """
        RESERVED = 0b11
        IN_USE = 0b10
        NOT_IN_USE = 0b01
        NOT_INDICATED = 0b00


    class BitStreamMode(Enum):
        """
        Dolby Digital Plus `bsmod` field
        § 4.3.2.2
        """

        COMPLETE_MAIN = 0b000
        "main audio service: complete main"

        MUSIC_AND_EFFECTS = 0b001
        "main audio service: music and effects"

        VISUALLY_IMPAIRED = 0b010
        "associated service: visually impaired"

        HEARING_IMPAIRED = 0b011
        "associated service: hearing impaired"

        DIALOGUE_ONLY = 0b100
        "associated service: dialogue"

        COMMENTARY = 0b101
        "associated service: commentary"

        EMERGENCY = 0b110
        "associated service: emergency"

        VOICEOVER_KARAOKE = 0b111
        """
        associated service: voice over *OR* main audio service: karaoke.
        If `acmod` is `0b001` (mono 1/0), this is voice-over, otherwise it
        should be interpreted as karaoke.
        """


    class AudioCodingMode(Enum):
        """
        Dolby Digital Plus `acmod` field
        § 4.3.2.3
        """
        RESERVED = 0b000
        CH_ORD_1_0 = 0b001
        "Mono"
        CH_ORD_2_0 = 0b010
        "L/R stereo"
        CH_ORD_3_0 = 0b011
        "LCR stereo"
        CH_ORD_2_1 = 0b100
        "LR + mono surround"
        CH_ORD_3_1 = 0b101
        "LCR + mono surround"
        CH_ORD_2_2 = 0b110
        "LR + LR surround"
        CH_ORD_3_2 = 0b111
        "LCR + LR surround"


    class CenterDownMixLevel(Enum):
        """
        § 4.3.3.1
        """

        DOWN_3DB = 0b00
        "Attenuate 3 dB"
    
        DOWN_45DB = 0b01
        "Attenuate 4.5 dB"
        
        DOWN_6DB = 0b10
        "Attenuate 6 dB"

        RESERVED = 0b11


    class SurroundDownMixLevel(Enum):
        """
        Dolby Digital Plus `surmixlev` field
        § 4.3.3.2
        """
        DOWN_3DB = 0b00
        DOWN_6DB = 0b01
        MUTE = 0b10
        RESERVED = 0b11


    class LanguageCode(int):
        """
        § 4.3.4.1

        Per ATSC/A52 § 5.4.2.12, this is not in use and always 0xFF.
        """
        pass


    class MixLevel(int):
        """
        § 4.3.6.2
        """
        pass


    class DialnormLevel(int):
        """
        § 4.3.4.4
        """
        pass


    class RoomType(Enum):
        """
        `roomtyp` 4.3.6.3
        """
        NOT_INDICATED = 0b00
        LARGE_ROOM_X_CURVE = 0b01
        SMALL_ROOM_FLAT_CURVE = 0b10
        RESERVED = 0b11


    class PreferredDownMixMode(Enum):
        """
        Indicates the creating engineer's preference of what the receiver should
        downmix.
        § 4.3.8.1
        """
        NOT_INDICATED = 0b00
        PRO_LOGIC = 0b01
        STEREO = 0b10
        PRO_LOGIC_2 = 0b11


    class SurroundEXMode(IntEnum):
        """
        Dolby Surround-EX mode.
        `dsurexmod` § 4.3.9.1
        """
        NOT_INDICATED = 0b00
        NOT_SEX = 0b01
        SEX = 0b10
        PRO_LOGIC_2 = 0b11


    class HeadphoneMode(IntEnum):
        """
        `dheadphonmod` § 4.3.9.2
        """
        NOT_INDICATED = 0b00
        NOT_DOLBY_HEADPHONE = 0b01
        DOLBY_HEADPHONE = 0b10
        RESERVED = 0b11


    class ADConverterType(Enum):
        STANDARD = 0
        HDCD = 1


    class StreamDependency(Enum):
        """
        Encodes `ddplus_info1.stream_type` field § 4.3.12.1
        """

        INDEPENDENT = 0
        DEPENDENT = 1
        INDEPENDENT_FROM_DOLBY_DIGITAL = 2
        RESERVED = 3


    class RFCompressionProfile(Enum):
        """
        `compr1` RF compression profile
        § 4.3.10 (fig 42)
        """
        NONE = 0
        FILM_STANDARD = 1
        FILM_LIGHT = 2
        MUSIC_STANDARD = 3
        MUSIC_LIGHT = 4
        SPEECH = 5

    #: Program ID number, this identifies the program in a multi-program 
    #: element. § 4.3.1
    program_id: int

    #: `True` if LFE is enabled. § 4.3.2.1
    lfe_on: bool

    #: The kind of service of this stream. `bsmod` § 4.3.2.2
    bitstream_mode: BitStreamMode

    #: Indicates which channels are in use. `acmod` § 4.3.2.3
    audio_coding_mode: AudioCodingMode

    #: When the front three channels are in use, gives the center
    #: downmix level. ``
    center_downmix_level: CenterDownMixLevel

    #: When the surround channels are in use, gives the surround
    #: downmix level.
    surround_downmix_level: SurroundDownMixLevel

    #: If the `acmod` is LR, this indicates if the channels
    #: are encoded in Dolby Surround.
    dolby_surround_encoded: DolbySurroundEncodingMode

    #: `True` if there is a langcode present in the metadata.
    langcode_present: bool

    #: `True` if this bitstream is copyrighted.
    copyright_bitstream: bool

    #: `True` if this bitstream is original.
    original_bitstream: bool

    dialnorm: DialnormLevel

    #: Language code
    langcode: int

    #: `True` if `mixlevel` and `roomtype` are valid
    prod_info_exists: bool

    #: Mix level
    mixlevel: MixLevel

    #: Room Type
    roomtype: RoomType

    #: LoRo preferred center downmix level
    loro_center_downmix_level: DownMixLevelToken
    
    #: LoRo preferred surround downmix level
    loro_surround_downmix_level: DownMixLevelToken

    #: Preferred downmix mode
    downmix_mode: PreferredDownMixMode
    
    #: LtRt preferred center downmix level
    ltrt_center_downmix_level: DownMixLevelToken

    #: LtRt preferred surround downmix level
    ltrt_surround_downmix_level: DownMixLevelToken

    #: Surround-EX mode
    surround_ex_mode: SurroundEXMode
    
    #: Dolby Headphone mode
    dolby_headphone_encoded: HeadphoneMode

    ad_converter_type: ADConverterType
    compression_profile: RFCompressionProfile
    dynamic_range: RFCompressionProfile
    
    #: Indicates if this stream can be decoded independently or not
    stream_dependency: StreamDependency

    #: Data rate of this bitstream in kilobits per second
    datarate_kbps: int
    
    @staticmethod
    def load(buffer: bytes):
        assert len(buffer) == 96, "Dolby Digital Plus segment incorrect size, "
        "expected 96 got %i" % len(buffer)

        def program_id(b) -> int:
            return b

        def program_info(b):
            return (b & 0x40) > 0, \
                DolbyDigitalPlusMetadata.BitStreamMode(b & 0x38 >> 3), \
                DolbyDigitalPlusMetadata.AudioCodingMode(b & 0x7)

        def ddplus_reserved1(_):
            pass

        def surround_config(b):
            return DolbyDigitalPlusMetadata.CenterDownMixLevel(b & 0x30 >> 4), \
                DolbyDigitalPlusMetadata.SurroundDownMixLevel(b & 0xc >> 2), \
                DolbyDigitalPlusMetadata.DolbySurroundEncodingMode(b & 0x3)

        def dialnorm_info(b):
            return (b & 0x80) > 0 , b & 0x40 > 0, b & 0x20 > 0, \
                DolbyDigitalPlusMetadata.DialnormLevel(b & 0x1f)

        def langcod(b) -> int:
            return b

        def audio_prod_info(b):
            return (b & 0x80) > 0, \
                DolbyDigitalPlusMetadata.MixLevel(b & 0x7c >> 2), \
                DolbyDigitalPlusMetadata.RoomType(b & 0x3)

        # loro_center_downmix_level, loro_surround_downmix_level 
        def ext_bsi1_word1(b):
            return DolbyDigitalPlusMetadata.DownMixLevelToken(b & 0x38 >> 3), \
                DolbyDigitalPlusMetadata.DownMixLevelToken(b & 0x7)

        # downmix_mode, ltrt_center_downmix_level, ltrt_surround_downmix_level
        def ext_bsi1_word2(b):
            return DolbyDigitalPlusMetadata.PreferredDownMixMode(b & 0xC0 >> 6), \
                DolbyDigitalPlusMetadata.DownMixLevelToken(b & 0x38 >> 3), \
                DolbyDigitalPlusMetadata.DownMixLevelToken(b & 0x7)

        #surround_ex_mode, dolby_headphone_encoded, ad_converter_type 
        def ext_bsi2_word1(b):
            return DolbyDigitalPlusMetadata.SurroundEXMode(b & 0x60 >> 5), \
                DolbyDigitalPlusMetadata.HeadphoneMode(b & 0x18 >> 3), \
                DolbyDigitalPlusMetadata.ADConverterType( b & 0x4 >> 2)

        def ddplus_reserved2(_):
            pass

        def compr1(b):
            return DolbyDigitalPlusMetadata.RFCompressionProfile(b)

        def dynrng1(b):
            DolbyDigitalPlusMetadata.RFCompressionProfile(b) 

        def ddplus_reserved3(_):
            pass

        def ddplus_info1(b):
            return DolbyDigitalPlusMetadata.StreamDependency(b & 0xc >> 2)

        def ddplus_reserved4(_):
            pass

        def datarate(b) -> int:
            return unpack("<H", b)[0]

        def reserved(_):
            pass

        pid = program_id(buffer[0])
        lfe_on, bitstream_mode, audio_coding_mode = program_info(buffer[1])
        ddplus_reserved1(buffer[2:2])
        center_downmix_level, surround_downmix_level, dolby_surround_encoded = surround_config(buffer[4])
        langcode_present, copyright_bitstream, original_bitstream, dialnorm = dialnorm_info(buffer[5])
        langcode = langcod(buffer[6])
        prod_info_exists, mixlevel, roomtype = audio_prod_info(buffer[7])

        loro_center_downmix_level, loro_surround_downmix_level = ext_bsi1_word1(buffer[8])
        downmix_mode, ltrt_center_downmix_level, ltrt_surround_downmix_level = ext_bsi1_word2(buffer[9])
        surround_ex_mode, dolby_headphone_encoded, ad_converter_type = ext_bsi2_word1(buffer[10])

        ddplus_reserved2(buffer[11:14])
        compression = compr1(buffer[14])
        dynamic_range = dynrng1(buffer[15])
        ddplus_reserved3(buffer[16:19])
        stream_info = ddplus_info1(buffer[19])
        ddplus_reserved4(buffer[20:25])
        data_rate = datarate(buffer[25:27])
        reserved(buffer[27:69])

        return DolbyDigitalPlusMetadata(program_id=pid,
            lfe_on=lfe_on, 
            bitstream_mode=bitstream_mode,
            audio_coding_mode=audio_coding_mode,
            center_downmix_level=center_downmix_level,
            surround_downmix_level=surround_downmix_level,
            dolby_surround_encoded=dolby_surround_encoded, 
            langcode_present=langcode_present, 
            copyright_bitstream=copyright_bitstream, 
            original_bitstream=original_bitstream,
            dialnorm=dialnorm, 
            langcode=langcode,
            prod_info_exists=prod_info_exists,
            mixlevel=mixlevel,
            roomtype=roomtype,
            loro_center_downmix_level=loro_center_downmix_level,
            loro_surround_downmix_level=loro_surround_downmix_level,
            downmix_mode=downmix_mode,
            ltrt_center_downmix_level=ltrt_center_downmix_level, 
            ltrt_surround_downmix_level=ltrt_surround_downmix_level,
            surround_ex_mode=surround_ex_mode,
            dolby_headphone_encoded=dolby_headphone_encoded,
            ad_converter_type=ad_converter_type,
            compression_profile=compression,
            dynamic_range=dynamic_range,
            stream_dependency=stream_info,
            datarate_kbps=data_rate)


@dataclass
class DolbyAtmosMetadata:
    """
    Dolby Atmos Metadata Segment

    https://github.com/DolbyLaboratories/dbmd-atmos-parser/
    """

    class WarpMode(Enum):
        NORMAL = 0x00
        WARPING = 0x01
        DOWNMIX_PLIIX = 0x02
        DOWNMIX_LORO = 0x03
        NOT_INDICATED = 0x04

    tool_name: str
    tool_version: Tuple[int,int,int]
    warp_mode: WarpMode

    SEGMENT_LENGTH = 248
    TOOL_NAME_LENGTH = 64

    @classmethod
    def load(cls, data: bytes):
        assert len(data) == cls.SEGMENT_LENGTH, "DolbyAtmosMetadata segment "\
            "is incorrect length, expected %i actual was %i" % (cls.SEGMENT_LENGTH, len(data)) 

        h = BytesIO(data)

        h.seek(32, 1)
        toolname = h.read(cls.TOOL_NAME_LENGTH)
        toolname = unpack("%is" % cls.TOOL_NAME_LENGTH, toolname)[0]
        toolname = toolname.decode('utf-8').strip('\0')

        vers = h.read(3)
        major, minor, fix = unpack("BBB", vers)

        h.seek(53, 1)

        a_val = unpack("B", h.read(1))[0]
        warp_mode = a_val & 0x7

        return DolbyAtmosMetadata(tool_name=toolname, 
            tool_version=(major, minor, fix), warp_mode=DolbyAtmosMetadata.WarpMode(warp_mode))

        
@dataclass
class DolbyAtmosSupplementalMetadata:
    """
    Dolby Atmos supplemental metadata segment.

    https://github.com/DolbyLaboratories/dbmd-atmos-parser/blob/master/dbmd_atmos_parse/src/dbmd_atmos_parse.c
    """ 

    class BinauralRenderMode(Enum):
        BYPASS = 0x00
        NEAR = 0x01
        FAR = 0x02
        MID = 0x03
        NOT_INDICATED = 0x04


    object_count: int
    render_modes: List['DolbyAtmosSupplementalMetadata.BinauralRenderMode']
    trim_modes: List[int]


    MAGIC = 0xf8726fbd
    TRIM_CONFIG_COUNT = 9

    @classmethod
    def load(cls, data: bytes):

        trim_modes = []
        render_modes = []

        h = BytesIO(data)
        magic = unpack("<I", h.read(4))
        assert magic == cls.MAGIC, "Magic value was not found"

        object_count = unpack("<H", h.read(2))

        h.read(1) #skip 1

        for _ in range(cls.TRIM_CONFIG_COUNT):
            auto_trim = unpack("B", h.read(1))
            trim_modes.append(auto_trim)

            h.read(14) #skip 14
        
        h.read(object_count) # skip object_count bytes

        for _ in range(object_count):
            binaural_mode = unpack("B", h.read(1))
            binaural_mode &= 0x7
            render_modes.append(binaural_mode)

        return DolbyAtmosSupplementalMetadata(object_count=object_count,
            render_modes=render_modes,trim_modes=trim_modes)


class WavDolbyMetadataReader:
    """
    Reads Dolby bitstream metadata.
    """

    #: List of the Dolby Metadata Segments.
    #:
    #: Each list entry is a tuple of `SegmentType`, a `bool`
    #: indicating if the segment's checksum was valid, and the
    #: segment's parsed dataclass (or a `bytes` array if it was 
    #: not recognized).
    segment_list: Tuple[Union[SegmentType, int], bool, Any] 

    version: Tuple[int,int,int,int]

    @staticmethod
    def segment_checksum(bs: bytes, size: int):
        retval = size
        for b in bs:
            retval += int(b)
            retval &= 0xff

        retval = ((~retval) + 1) & 0xff

        return retval


    def __init__(self, dbmd_data) -> None:
        self.segment_list = []

        h = BytesIO(dbmd_data)

        v_vec = []
        for _ in range(4):
            b = h.read(1)
            v_vec.insert(0, unpack("B",b)[0])
        
        self.version = tuple(v_vec)

        while True:
            stype= SegmentType(unpack("B", h.read(1))[0])
            if stype == SegmentType.EndMarker:
                break
            else:
                seg_size = unpack("<H", h.read(2))[0]
                seg_payload = h.read(seg_size)
                expected_checksum = WavDolbyMetadataReader.segment_checksum(seg_payload, seg_size)
                checksum = unpack("B", h.read(1))[0]

                segment = seg_payload
                if stype == SegmentType.DolbyDigitalPlus:
                    segment = DolbyDigitalPlusMetadata.load(segment)
                elif stype == SegmentType.DolbyAtmos:
                    segment = DolbyAtmosMetadata.load(segment)
                # elif stype == SegmentType.DolbyAtmosSupplemental:
                #     segment = DolbyAtmosSupplementalMetadata.load(segment)
                
                self.segment_list.append( (stype, checksum == expected_checksum, segment) )
    
    def dolby_digital_plus(self) -> List[DolbyDigitalPlusMetadata]:
        """
        Every valid Dolby Digital Plus metadata segment in the file.
        """
        return [x[2] for x in self.segment_list \
            if x[0] == SegmentType.DolbyDigitalPlus and x[1]]

    def dolby_atmos(self) -> List[DolbyAtmosMetadata]:
        """
        Every valid Dolby Atmos metadata segment in the file.
        """
        return [x[2] for x in self.segment_list \
            if x[0] == SegmentType.DolbyAtmos and x[1]]

    # def dolby_atmos_supplemental(self) -> List[DolbyAtmosSupplementalMetadata]:
    #     """
    #     Every valid Dolby Atmos Supplemental metadata segment in the file.
    #     """
    #     return [x[2] for x in self.segment_list \
    #         if x[0] == SegmentType.DolbyAtmosSupplemental and x[1]]

    def to_dict(self) -> dict:

        ddp = map(lambda x: asdict(x), self.dolby_digital_plus())
        atmos = map(lambda x: asdict(x), self.dolby_atmos())
        #atmos_sup = map(lambda x: asdict(x), self.dolby_atmos_supplemental())
        
        return dict(dolby_digital_plus=list(ddp),
             dolby_atmos=list(atmos))
