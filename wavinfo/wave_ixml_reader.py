import xml.etree.ElementTree as ET

class WavIXMLFormat:
    """
    iXML recorder metadata, as defined by iXML 2.0
    """
    def __init__(xml):
        self.source = xml
        self.parsed = ET.fromstring(xml)

    def _get_text_value(xpath):
        root = self.parsed.getroot()
        e = root.find("//BWFXML/" + xpath)
        if e:
            return e.text
    
    @property
    def project(self):
        return _get_text_value("PROJECT")
        
    @property
    def scene(self):
        return _get_text_value("SCECE")

    @property
    def take(self):
        return _get_text_value("TAKE")

    @property
    def tape(self):
        return _get_text_value("TAPE")

    @property
    def family_uid(self):
        return _get_text_value("FILE_SET/FAMILY_UID")

    @property
    def family_name(self):
        return _get_text_value("FILE_SET/FAMILY_NAME")


