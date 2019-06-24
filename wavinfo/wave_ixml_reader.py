#import xml.etree.ElementTree as ET
from lxml import etree as ET
import io

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
        xmlBytes = io.BytesIO(xml)
        try:
            parser = ET.XMLParser(recover=True)
            self.parsed = ET.parse(xmlBytes, parser=parser)
        except ET.ParseError as err:
            print("Error parsing iXML: " + str(err))
            decoded = xml.decode(encoding='utf_8_sig')
            print(decoded)
            self.parsed = ET.parse(io.StringIO(decoded))

    def _get_text_value(self, xpath):
        e = self.parsed.find("./" + xpath)
        if e is not None:
            return e.text

    @property
    def project(self):
        """
        The project/film name entered for the recording.
        """
        return self._get_text_value("PROJECT")

    @property
    def scene(self):
        """
        Scene/slate.
        """
        return self._get_text_value("SCENE")

    @property
    def take(self):
        """
        Take number.
        """
        return self._get_text_value("TAKE")

    @property
    def tape(self):
        """
        Tape name.
        """
        return self._get_text_value("TAPE")

    @property
    def family_uid(self):
        """
        The globally-unique ID for this file family. This may be in the format
        of a GUID, or an EBU Rec 9 source identifier, or some other dumb number.
        """
        return self._get_text_value("FILE_SET/FAMILY_UID")

    @property
    def family_name(self):
        """
        The name of this file's file family.
        """
        return self._get_text_value("FILE_SET/FAMILY_NAME")


