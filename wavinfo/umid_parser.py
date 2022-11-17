from functools import reduce


def binary_to_string(binary_value):
    return reduce(lambda val, el: val + "{:02x}".format(el), binary_value, '')


class UMIDParser:
    """
    Parse a raw binary SMPTE 330M Universal Materials Identifier

    This implementation is based on SMPTE ST 330:2011
    """
    def __init__(self, raw_umid: bytes):
        self.raw_umid = raw_umid
    #
    # @property
    # def universal_label(self) -> bytearray:
    #     return self.raw_umid[0:12]
    #
    # @property
    # def basic_umid(self):
    #     return self.raw_umid[0:32]

    def basic_umid_to_str(self):
        return binary_to_string(self.raw_umid[0:32])
    #
    # @property
    # def universal_label_is_valid(self) -> bool:
    #     valid_preamble = b'\x06\x0a\x2b\x34\x01\x01\x01\x05\x01\x01'
    #     return self.universal_label[0:len(valid_preamble)] == valid_preamble
    #
    # @property
    # def material_type(self) -> str:
    #     material_byte = self.raw_umid[10]
    #     if material_byte == 0x1:
    #         return 'picture'
    #     elif material_byte == 0x2:
    #         return 'audio'
    #     elif material_byte == 0x3:
    #         return 'data'
    #     elif material_byte == 0x4:
    #         return 'other'
    #     elif material_byte == 0x5:
    #         return 'picture_single_component'
    #     elif material_byte == 0x6:
    #         return 'picture_multiple_component'
    #     elif material_byte == 0x7:
    #         return 'audio_single_component'
    #     elif material_byte == 0x9:
    #         return 'audio_multiple_component'
    #     elif material_byte == 0xb:
    #         return 'auxiliary_single_component'
    #     elif material_byte == 0xc:
    #         return 'auxiliary_multiple_component'
    #     elif material_byte == 0xd:
    #         return 'mixed_components'
    #     elif material_byte == 0xf:
    #         return 'not_identified'
    #     else:
    #         return 'not_recognized'
    #
    # @property
    # def material_number_creation_method(self) -> str:
    #     method_byte = self.raw_umid[11]
    #     method_byte = (method_byte << 4) & 0xf
    #     if method_byte == 0x0:
    #         return 'undefined'
    #     elif method_byte == 0x1:
    #         return 'smpte'
    #     elif method_byte == 0x2:
    #         return 'uuid'
    #     elif method_byte == 0x3:
    #         return 'masked'
    #     elif method_byte == 0x4:
    #         return 'ieee1394'
    #     elif 0x5 <= method_byte <= 0x7:
    #         return 'reserved_undefined'
    #     else:
    #         return 'unrecognized'
    #
    # @property
    # def instance_number_creation_method(self) -> str:
    #     method_byte = self.raw_umid[11]
    #     method_byte = method_byte & 0xf
    #     if method_byte == 0x0:
    #         return 'undefined'
    #     elif method_byte == 0x01:
    #         return 'local_registration'
    #     elif method_byte == 0x02:
    #         return '24_bit_prs'
    #     elif method_byte == 0x03:
    #         return 'copy_number_and_16_bit_prs'
    #     elif 0x04 <= method_byte <= 0x0e:
    #         return 'reserved_undefined'
    #     elif method_byte == 0x0f:
    #         return 'live_stream'
    #     else:
    #         return 'unrecognized'
    #
    # @property
    # def indicated_length(self) -> str:
    #     if self.raw_umid[12] == 0x13:
    #         return 'basic'
    #     elif self.raw_umid[12] == 0x33:
    #         return 'extended'
    #
    # @property
    # def instance_number(self) -> bytearray:
    #     return self.raw_umid[13:3]
    #
    # @property
    # def material_number(self) -> bytearray:
    #     return self.raw_umid[16:16]
    #
    # @property
    # def source_pack(self) -> Union[bytearray, None]:
    #     if self.indicated_length == 'extended':
    #         return self.raw_umid[32:32]
    #     else:
    #         return None
