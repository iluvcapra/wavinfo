# Dolby RMU Metadata per EBU Tech 3285 Supp 6
#
# https://tech.ebu.ch/docs/tech/tech3285s6.pdf
#

from struct import unpack, calcsize
from enum import (Enum, IntEnum)

CHUNK_IDENT = "dbmd"
DOLBY_VERSION = "1.0.0.6"


class _DPPGenericDownMixLevel(Enum):
    PLUS_3DB = 0b000
    PLUS_1_5DB = 0b001
    UNITY = 0b010
    MINUS_1_5DB = 0b011
    MINUS_3DB = 0b100
    MINUS_4_5DB = 0b101
    MINUS_6DB = 0b110
    MUTE = 0b111


class DPPDolbySurroundEncodingMode(Enum):
    RESERVED = 0b11
    IN_USE = 0b10
    NOT_IN_USE = 0b01
    NOT_INDICATED = 0b00

# DPPLoRoDownMixCenterLevel
# DPPLtRtCenterMixLevel
# DPPLtRtSurroundMixLevel

class DolbyMetadataSegmentTypes(IntEnum):
    END_MARKER = 0
    DOLBY_E_METADATA = 1
    DOLBY_DIGITAL_METADATA = 3
    DOLBY_DIGITAL_PLUS_METADATA = 7
    AUDIO_INFO = 8


class DDPBitStreamMode(Enum):
    """
    Dolby Digital Plus `bsmod` field
    § 4.3.2.2
    """
    COMPLETE_MAIN = 0b000
    MUSIC_AND_EFFECTS = 0b001
    VISUALLY_IMPAIRED = 0b010
    HEARING_IMPAIRED = 0b011
    DIALOGUE_ONLY = 0b100
    COMMENTARY = 0b101
    EMERGENCY = 0b110
    VOICEOVER = 0b111 # if audioconfigmode is 1_0
    KARAOKE = 0b1000  # if audioconfigmode is not 1_0


class DDPAudioCodingMode(Enum):
    """
    Dolby Digital Plus `acmod` field
    § 4.3.2.3
    """
    RESERVED = 0b000
    CH_ORD_1_0 = 0b001
    CH_ORD_2_0 = 0b010
    CH_ORD_3_0 = 0b011
    CH_ORD_2_1 = 0b100
    CH_ORD_3_1 = 0b101
    CH_ORD_2_2 = 0b110
    CH_ORD_3_2 = 0b111


class DPPCenterDownMixLevel(Enum):
    """
    § 4.3.3.1
    """
    DOWN_3DB = 0b00
    DOWN_45DB = 0b01
    DOWN_6DB = 0b10
    RESERVED = 0b11


class DPPSurroundDownMixLevel(Enum):
    """
    Dolby Digital Plus `surmixlev` field
    § 4.3.3.2
    """
    DOWN_3DB = 0b00
    DOWN_6DB = 0b01
    MUTE = 0b10
    RESERVED = 0b11


class DPPLanguageCode(Enum):
    """
    § 4.3.4.1 , 4.3.5 (always 0xFF)
    """
    # this is removed in https://www.atsc.org/wp-content/uploads/2015/03/A52-201212-17.pdf § 5.4.2.12
    # It should just be 0xff
    pass


class DPPMixLevel(int):
    pass


class DPPDialnormLevel(int):
    pass


class DPPRoomTime(Enum):
    """
    `roomtyp` 4.3.6.3
    """
    NOT_INDICATED = 0b00
    LARGE_ROOM_X_CURVE = 0b01
    SMALL_ROOM_FLAT_CURVE = 0b10
    RESERVED = 0b11


class DPPPreferredDownMixMode(Enum):
    """
    § 4.3.8.1
    """
    NOT_INDICATED = 0b00
    PRO_LOGIC = 0b01
    STEREO = 0b10
    PRO_LOGIC_2 = 0b11


# class DPPLtRtCenterMixLevel(_DPPGenericDownMixLevel):
#     pass
#
#
# class DPPLtRtSurroundMixLevel(_DPPGenericDownMixLevel):
#     pass
#
#
# class DPPSurroundEXMode(_DPPGenericInUseIndicator):
#     pass
#
#
# class DPPHeadphoneMode(_DPPGenericInUseIndicator):
#     pass


class DPPADConverterType(Enum):
    STANDARD = 0
    HDCD = 1


class DDPStreamDependency(Enum):
    """
    Encodes `ddplus_info1.stream_type` field § 4.3.12.1
    """
    INDEPENDENT = 0
    DEPENDENT = 1
    INDEPENDENT_FROM_DOLBY_DIGITAL = 2
    RESERVED = 3


class DDPDataRate(int):
    pass


class DPPRFCompressionProfile(Enum):
    NONE = 0
    FILM_STANDARD = 1
    FILM_LIGHT = 2
    MUSIC_STANDARD = 3
    MUSIC_LIGHT = 4
    SPEECH = 5


class DolbyDigitalPlusMetadata:

    @classmethod
    def parse(cls, binary_data):
        binary_format = "<BBxxBBBBBBBBBBBBBxxxBxxxxxH"
        assert len(binary_data >= calcsize(binary_format))
        fields = unpack(binary_format, binary_data)


class WavDolbyReader:
    def __init__(self, dolby_data):
        version, remainder = unpack("<U", dolby_data[0]), dolby_data[1:]

        ## FIXME continues...