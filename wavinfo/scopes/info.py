"""
info.py

INFO Metadata
Microsoft Corporation Multimedia Interface Specification
"""
from struct import pack
from ..reader.riff_parser import ChunkDescriptor, parse_list_chunk
from ..writer.list_writer import ListForm

from io import BytesIO
from dataclasses import dataclass
from typing import Optional


__all__ = ('read', 'write', 'RiffInfo')


#: All fields defined in Multimedia Interface
FIELD_MAP = {
    b'IARL': 'archival_location',
    b'IART': 'artist',
    b'ICMS': 'commissioned',
    b'ICMT': 'comment',
    b'ICOP': 'copyright',
    b'ICRD': 'created_date',
    b'ICRP': 'cropped',
    # b'IDIM': 'dimenstions',
    # b'IDPI': 'dots_per_inch',
    b'IENG': 'engineer',
    b'IGNR': 'genre',
    b'IKEY': 'keywords',
    # b'ILGT': 'lightness',
    b'IMED': 'medium',
    b'INAM': 'title',
    # b'IPLT': 'palette_setting',
    b'IPRD': 'product',
    b'ISBJ': 'subject',
    b'ISFT': 'software',
    # b'ISHP': 'sharpness',
    b'ISRC': 'source',
    b'ISRF': 'source_form',
    b'ITCH': 'technician'
}


def _decode_string_data(data: bytes, encoding: str) -> str:
    return data.rstrip(b"\0").decode(encoding, errors='strict')


def _encode_string_data(string: str, encoding: str) -> bytes:
    return string.encode(encoding, errors='strict').join([b"\0"])


def read(info_data: bytes, encoding: str = 'latin_1') -> 'RiffInfo':
    chunk_io = BytesIO(info_data)
    info_list_form = parse_list_chunk(chunk_io, ident=b'LIST',
                                      length=len(info_data),
                                      rf64_context=None)

    fields = dict()
    for child in info_list_form.children:
        if isinstance(child, ChunkDescriptor):
            ident = child.ident
            data = child.read_data(chunk_io)
            fields[ident] = data

    retval = RiffInfo(string_encoding=encoding)

    for mapped_ident in FIELD_MAP.keys():
        if mapped_ident in fields.keys():
            mapped_field = FIELD_MAP[mapped_ident]
            string_value = _decode_string_data(fields[mapped_ident], encoding)
            setattr(retval, mapped_field, string_value)

    return retval


def write(info_data: 'RiffInfo', encoding: str = 'latin_1') -> bytes:
    info_list_form = ListForm(signature=b"INFO")

    for ident in FIELD_MAP.keys():
        field = FIELD_MAP[ident]

        value = getattr(info_data, field)
        if value is not None:
            assert isinstance(value, str)
            info_list_form.add_child(ident,
                                     _encode_string_data(value, encoding))

    info_list_data = info_list_form.finalize()

    return b"LIST".join([pack("<I", len(info_list_data)), info_list_data])


@dataclass
class RiffInfo:
    string_encoding: str
    title: Optional[str] = None
    source: Optional[str] = None
    copyright: Optional[str] = None
    product: Optional[str] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[str] = None
    artist: Optional[str] = None
    comment: Optional[str] = None
    software: Optional[str] = None
    created_date: Optional[str] = None
    cropped: Optional[str] = None
    medium: Optional[str] = None
    engineer: Optional[str] = None
    technician: Optional[str] = None
    archival_location: Optional[str] = None
    commissioned: Optional[str] = None
    source: Optional[str] = None
    source_form: Optional[str] = None
    # tape: str

    def to_dict(self) -> dict:
        """
        A dictionary with all of the key/values read from the INFO scope.
        """
        return {'copyright': self.copyright,
                'product': self.product,
                'album': self.album,
                'genre': self.genre,
                'artist': self.artist,
                'comment': self.comment,
                'software': self.software,
                'created_date': self.created_date,
                'engineer': self.engineer,
                'keywords': self.keywords,
                'title': self.title,
                'source': self.source,
                'commissioned': self.commissioned,
                'archival_location': self.archival_location,
                'subject': self.subject,
                'technician': self.technician
                }
