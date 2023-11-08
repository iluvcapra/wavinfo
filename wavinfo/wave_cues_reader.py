"""
Cues metadata

For reference on implementation of cues and related metadata see: 
August 1991, "Multimedia Programming Interface and Data Specifications 1.0",
IBM Corporation and Microsoft Corporation

https://www.aelius.com/njh/wavemetatools/doc/riffmci.pdf
"""
from dataclasses import dataclass
import encodings
from .riff_parser import ChunkDescriptor

from struct import unpack, calcsize
from typing import Optional, Tuple,  NamedTuple, List, Dict, Any, Generator

#: Country Codes used in the RIFF standard to resolve locale. These codes 
#: appear in CSET and LTXT metadata.
CountryCodes = """000 None Indicated
001,USA
002,Canada
003,Latin America
030,Greece 
031,Netherlands
032,Belgium
033,France
034,Spain
039,Italy
041,Switzerland
043,Austria
044,United Kingdom
045,Denmark
046,Sweden
047,Norway
049,West Germany
052,Mexico
055,Brazil
061,Australia
064,New Zealand
081,Japan
082,Korea
086,People’s Republic of China
088,Taiwan
090,Turkey
351,Portugal
352,Luxembourg
354,Iceland 
358,Finland"""

#: Language and Dialect codes used in the RIFF standard to resolve native 
#: language of text fields. These codes appear in CSET and LTXT metadata.
LanguageDialectCodes = """0 0 None Indicated
1,1,Arabic
2,1,Bulgarian
3,1,Catalan
4,1,Traditional Chinese 
4,2,Simplified Chinese 
5,1,Czech
6,1,Danish
7,1,German
7,2,Swiss German 
8,1,Greek
9,1,US English
9,2,UK English 
10,1,Spanish
10,2,Spanish Mexican 
11,1,Finnish
12,1,French
12,2,Belgian French 
12,3,Canadian French 
12,4,Swiss French 
13,1,Hebrew 
14,1,Hungarian
15,1,Icelandic
16,1,Italian
16,2,Swiss Italian 
17,1,Japanese
18,1,Korean
19,1,Dutch
19,2,Belgian Dutch 
20,1,Norwegian - Bokmal 
20,2,Norwegian - Nynorsk 
21,1,Polish
22,1,Brazilian Portuguese 
22,2,Portuguese 
23,1,Rhaeto-Romanic 
24,1,Romanian
25,1,Russian
26,1,Serbo-Croatian (Latin) 
26,2,Serbo-Croatian (Cyrillic) 
27,1,Slovak
28,1,Albanian
29,1,Swedish
30,1,Thai
31,1,Turkish
32,1,Urdu
33,1,Bahasa"""


class CueEntry(NamedTuple):
    name: int
    position: int
    chunk_id: bytes
    chunk_start: int
    block_start: int
    sample_offset: int

    Format = "<II4sIII"
    
    @classmethod
    def format_size(cls) -> int:
        return calcsize(cls.Format)

    @classmethod
    def read(cls, data: bytes) -> 'CueEntry':
        assert len(data) == cls.format_size(), \
            f"cue data size incorrect, expected {calcsize(cls.Format)} found {len(data)}"

        parsed = unpack(cls.Format, data)

        return cls(name=parsed[0], position=parsed[1], chunk_id=parsed[2],
                   chunk_start=parsed[3], block_start=parsed[4], 
                   sample_offset=parsed[5])


class LabelEntry(NamedTuple):
    name: int
    text: str

    @classmethod
    def read(cls, data: bytes, encoding: str):
        return cls(name=unpack("<I", data[0:4])[0],
                   text=data[4:].decode(encoding).rstrip("\0"))


NoteEntry = LabelEntry


class RangeLabel(NamedTuple):
    name: int
    length: int
    purpose: str
    country: int
    language: int
    dialect: int
    codepage: int
    text: str

    @classmethod
    def read(cls, data: bytes, fallback_encoding: str):
        leader_struct_fmt = "<II4sHHHH"
        parsed = unpack(leader_struct_fmt, data[0:calcsize(leader_struct_fmt)])
        text_data = data[calcsize(leader_struct_fmt):]

        if data[6] != 0:
            fallback_encoding = f"cp{data[6]}"

        return cls(name=parsed[0], length=parsed[1], purpose=parsed[2],
                   country=parsed[3], language=parsed[4], 
                   dialect=parsed[5], codepage=parsed[6], 
                   text=text_data.decode(fallback_encoding))


@dataclass
class WavCuesReader:
    cues: List[CueEntry]
    labels: List[LabelEntry]
    ranges: List[RangeLabel]
    notes: List[NoteEntry]

    @classmethod
    def read_all(cls, f,
              cues: Optional[ChunkDescriptor], 
              labls: List[ChunkDescriptor],
              ltxts: List[ChunkDescriptor], 
              notes: List[ChunkDescriptor],
              fallback_encoding: str) -> 'WavCuesReader':
        
        cue_list = []
        if cues is not None:
            cues_data = cues.read_data(f)
            assert len(cues_data) >= 4, "cue metadata too short"
            offset = calcsize("<I")
            cues_count = unpack("<I", cues_data[0:offset])
            
            for _ in range(cues_count[0]):
                cue_bytes = cues_data[offset: offset + CueEntry.format_size()]
                cue_list.append(CueEntry.read(cue_bytes))
                offset += CueEntry.format_size()

        label_list = []
        for labl in labls:
            label_list.append(
                LabelEntry.read(labl.read_data(f), 
                                encoding=fallback_encoding)
            )

        range_list = []
        for r in ltxts:
            range_list.append(
                RangeLabel.read(r.read_data(f), 
                                fallback_encoding=fallback_encoding)
            )

        note_list = []
        for note in notes:
            note_list.append(
                NoteEntry.read(note.read_data(f),
                               encoding=fallback_encoding)
            )

        return WavCuesReader(cues=cue_list, labels=label_list,
                             ranges=range_list, notes=note_list)

    def each_cue(self) -> Generator[Tuple[int, int], None, None]:
        """
        Iterate through each cue. 

        :yields: the cue's ``name`` and ``sample_offset``
        """
        for cue in self.cues:
            yield (cue.name, cue.sample_offset)

    def label_and_note(self, cue_ident: int) -> Tuple[Optional[str],
                                                      Optional[str]]: 
        """
        Get the label and note (extended comment) for a cue.

        :param cue_ident: the cue's name, its unique identifying number
        :returns: a tuple of the the cue's label (if present) and note (if
            present) 
        """
        label = next((l.text for l in self.labels 
                      if l.name == cue_ident), None)
        note = next((n.text for n in self.notes 
                     if n.name == cue_ident), None)
        return (label, note)

    def range(self, cue_ident: int) -> Optional[int]:
        """
        Get the length of the time range for a cue, if it has one.

        :param cue_ident: the cue's name, its unique identifying number
        :returns: the length of the marker's range, or `None`
        """
        return next((r.length for r in self.ranges 
                     if r.name == cue_ident), None)

    def to_dict(self) -> Dict[str, Any]:
        retval = dict()

        for n, t in self.each_cue():
            retval[n] = dict()
            retval[n]['frame'] = t
            label, note = self.label_and_note(n)
            r = self.range(n)

            if label is not None:
                retval[n]['label'] = label
            if note is not None:
                retval[n]['note'] = note  
            if r is not None:
                retval[n]['length'] = r 
        
        return retval 
        # return dict(cues=[c._asdict() for c in self.cues],
        #             labels=[l._asdict() for l in self.labels],
        #             ranges=[r._asdict() for r in self.ranges],
        #             notes=[n._asdict() for n in self.notes])



