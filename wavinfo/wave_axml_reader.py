"""
ADM Reader
"""

from struct import unpack, unpack_from, calcsize
from dataclasses import dataclass

from lxml import etree as ET

@dataclass
class ChannelEntry:
    """
    A `chna` chunk table entry.
    """

    track_index: int
    "Track index (indexed from 1)"

    uid: str
    "audioTrackUID"

    track_ref: str
    "audioTrackFormatID"

    pack_ref: str
    "audioPackFormatID"


class WavAxmlReader:
    """
    Reads XML data from an EBU ADM (Audio Definiton Model) WAV File.
    """

    def __init__(self, axml_data: bytes, chna_data: bytes) -> None:
        header_fmt = "<HH"
        uid_fmt = "<H12s14s11sx"

        self.axml = ET.fromstring(axml_data)

        self.track_count, uid_count = unpack(header_fmt, chna_data)

        self.channel_uids = []

        offset = calcsize(header_fmt)
        for _ in range(uid_count):

            track_index, uid, track_ref, pack_ref = unpack_from(uid_fmt, chna_data, offset)

            # these values are either ascii or all null

            self.channel_uids.append(ChannelEntry(track_index,
                uid.decode('ascii') , track_ref.decode('ascii'), pack_ref.decode('ascii')))

            offset += calcsize(uid_fmt)
