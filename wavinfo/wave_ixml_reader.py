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

    def xml_str(self) -> str:
        return ET.tostring(self.parsed).decode("utf-8")

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

        :yields: `IXMLTrack` for each track.
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

    def to_dict(self):
        return dict(track_list=list(map(lambda x: x._asdict(), self.track_list)), 
            project=self.project,
            scene=self.scene,
            take=self.take,
            tape=self.tape,
            family_uid=self.family_uid,
            family_name=self.family_name 
            )

# Nuendo Audio Speaker Arrangement Codes
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 5.0.wav
# 18
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Atmos 5.1.4.wav
# 36
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 7.1 SDDS.wav
# 26
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 7.0 SDDS.wav
# 24
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 5.1.wav
# 19
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 7.1.wav
# 27
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Atmos 7.0.2.wav
# 48
#  tests/test_files/nuendo//wavinfo Test Project - Audio - LRCS.wav
# 14
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 7.0.wav
# 25
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 6.0 Music.wav
# 23
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Atmos 7.1.2.wav
# 33
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Atmos 5.0.4.wav
# 35
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Mono.wav
# 0
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Quad.wav
# 15
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Atmos 7.1.4.wav
# 44
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 6.1 Music.wav
# 23
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Stereo.wav
# 1
#  tests/test_files/nuendo//wavinfo Test Project - Audio - LRC.wav
# 10
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Atmos 7.1.6.wav
# 51
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Auro3d 13.1.wav
# 42
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Auro3d 13.0.wav
# 41
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Auro3d 11.0.wav
# 39
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Auro3d 11.1.wav
# 40
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 6.1 Surround EX.wav
# 22
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 2OA.wav
# 46
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Auro3d 10.0.wav
# 37
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Auro3d 10.1.wav
# 38
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 6.0 Surround EX.wav
# 20
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 3OA.wav
# 47
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Atmos 9.1.4.wav
# 53
#  tests/test_files/nuendo//wavinfo Test Project - Audio - Atmos 9.1.6.wav
# 55
#  tests/test_files/nuendo//wavinfo Test Project - Audio - 1OA.wav
# 45

# Nuendo Keys
# AudioSampleFormatSize, AudioSpeakerArrangement, MediaCompany, MediaDropFrames, MediaDuration(float) (seconds, session length?), 
# MediaStartTime(float), MediaTrackTitle, ProgramName, ProgramVersion, 