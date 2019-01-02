import xml.etree.ElementTree as ET
import io

class WavIXMLFormat:
    """
    iXML recorder metadata, as defined by iXML 2.0
    """
    def __init__(self, xml):
        self.source = xml
        xmlBytes = io.BytesIO(xml)
        self.parsed = ET.parse(xmlBytes)

    def _get_text_value(self, xpath):
        e = self.parsed.find("./" + xpath)
        if e is not None:
            return e.text

    @property
    def project(self):
        return self._get_text_value("PROJECT")

    @property
    def scene(self):
        return self._get_text_value("SCENE")

    @property
    def take(self):
        return self._get_text_value("TAKE")

    @property
    def tape(self):
        return self._get_text_value("TAPE")

    @property
    def family_uid(self):
        return self._get_text_value("FILE_SET/FAMILY_UID")

    @property
    def family_name(self):
        return self._get_text_value("FILE_SET/FAMILY_NAME")


