from lxml import etree as ET
import io
from collections import namedtuple
from typing import Optional

IXMLTrack = namedtuple('IXMLTrack', ['channel_index', 'interleave_index', 'name', 'function'])


class WavIXMLFormat:
    """
    iXML recorder metadata.
    """
    def __init__(self, xml):
        """
        Parse iXML.
        :param xml: A bytes-like object containing the iXML payload.
        """
        self.source = xml
        xml_bytes = io.BytesIO(xml)
        parser = ET.XMLParser(recover=True)
        self.parsed = ET.parse(xml_bytes, parser=parser)

    def _get_text_value(self, xpath) -> Optional[str]:
        e = self.parsed.find("./" + xpath)
        if e is not None:
            return e.text
        else: 
            return None

    @property
    def raw_xml(self):
        """
        The root entity of the iXML document.
        """
        return self.parsed

    @property
    def track_list(self):
        """
        A description of each track.
        :return: An Iterator
        """
        for track in self.parsed.find("./TRACK_LIST").iter():
            if track.tag == 'TRACK':
                yield IXMLTrack(channel_index=track.xpath('string(CHANNEL_INDEX/text())'),
                                interleave_index=track.xpath('string(INTERLEAVE_INDEX/text())'),
                                name=track.xpath('string(NAME/text())'),
                                function=track.xpath('string(FUNCTION/text())'))

    @property
    def project(self) -> Optional[str]:
        """
        The project/film name entered for the recording.
        """
        return self._get_text_value("PROJECT")

    @property
    def scene(self) -> Optional[str]:
        """
        Scene/slate.
        """
        return self._get_text_value("SCENE")

    @property
    def take(self) ->  Optional[str]:
        """
        Take number.
        """
        return self._get_text_value("TAKE")

    @property
    def tape(self) -> Optional[str]:
        """
        Tape name.
        """
        return self._get_text_value("TAPE")

    @property
    def family_uid(self) -> Optional[str]:
        """
        The globally-unique ID for this file family. This may be in the format
        of a GUID, or an EBU Rec 9 source identifier, or some other dumb number.
        """
        return self._get_text_value("FILE_SET/FAMILY_UID")

    @property
    def family_name(self) -> Optional[str]:
        """
        The name of this file's file family.
        """
        return self._get_text_value("FILE_SET/FAMILY_NAME")
