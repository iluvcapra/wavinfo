"""
Cues metadata

For reference on implementation of cues and related metadata see:
August 1991, "Multimedia Programming Interface and Data Specifications 1.0",
IBM Corporation and Microsoft Corporation

https://www.aelius.com/njh/wavemetatools/doc/riffmci.pdf
"""

from dataclasses import dataclass
from struct import iter_unpack, unpack, calcsize
from functools import reduce
from typing import (Iterable, Optional, Tuple, NamedTuple, Dict, Any,
                    Generator, List)

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


def read(cues_data: Optional[bytes], adtl_data: Optional[bytes],
         encoding: str) -> 'CueList':

    def _read_cues() -> Iterable['CueEntry']:
        if cues_data is None:
            return iter([])

        FORMAT = "<II4sIII"
        cue_count, = unpack("<I", cues_data[0:4])
        assert cue_count * calcsize(FORMAT) >= len(cues_data[4:])

        return map(lambda t: CueEntry(name=t[0], position=t[1], chunk_id=t[2],
                                      chunk_start=t[3], block_start=t[4],
                                      sample_offset=t[5]),
                   iter_unpack(FORMAT, cues_data[4:])
                   )

    def _traverse_adtl() -> Iterable[Tuple[bytes, bytes]]:
        """
        Iterate each child and payload
        """
        if adtl_data is None:
            return iter([])

        offset = 4
        while offset < len(adtl_data):
            fourcc, size = unpack("<4sI", adtl_data[offset:offset + 8])
            offset += 8
            yield (fourcc, adtl_data[offset: offset + size])
            offset += size
            if offset % 2 > 0:
                offset += 1

    def _decode_tagged_label(data: bytes) -> Tuple[int, str]:
        return (unpack("<I", data[0:4])[0],
                data[4:].rstrip(b"\0").decode(encoding)
                )

    def _read_labels() -> Iterable['LabelEntry']:
        labels = filter(lambda x: x[0] == b'labl', _traverse_adtl())
        label_params = map(lambda x: _decode_tagged_label(x[1]), labels)
        return map(lambda x: LabelEntry(name=x[0], text=x[1]), label_params)

    def _read_notes() -> Iterable['NoteEntry']:
        labels = filter(lambda x: x[0] == b'note', _traverse_adtl())
        label_params = map(lambda x: _decode_tagged_label(x[1]), labels)
        return map(lambda x: NoteEntry(name=x[0], text=x[1]), label_params)

    def _read_ranges() -> Iterable['RangeLabel']:
        ltxts = filter(lambda x: x[0] == b"ltxt", _traverse_adtl())
        FORMAT = "<II4sHHHH"
        format_length = calcsize(FORMAT)
        params_iter = map(lambda x: (unpack(FORMAT, x[1][0:format_length]),
                                     x[1][format_length:]), ltxts)

        return map(
            lambda x: RangeLabel(
                name=x[0][0],
                length=x[0][1],
                purpose=x[0][2],
                country=x[0][3],
                language=x[0][4],
                dialect=x[0][5],
                codepage=x[0][6],
                text=x[1].rstrip(b"\0") .decode(encoding)),
            params_iter)

    def _dict_reducer(acc: dict, obj) -> dict:
        acc[obj.name] = obj
        return acc

    return CueList(encoding=encoding,
                   cues=reduce(_dict_reducer, _read_cues(), dict()),
                   labels=list(_read_labels()),
                   notes=list(_read_notes()),
                   ranges=list(_read_ranges())
                   )


@dataclass
class CueList:
    encoding: str
    cues: Dict[int, 'CueEntry']
    labels: List['LabelEntry']
    notes: List['NoteEntry']
    ranges: List['RangeLabel']

    def each_cue(self) -> Generator[Tuple[int, int], None, None]:
        """
        Iterate through each cue.

        :yields: the cue's ``name`` and ``sample_offset``
        """
        for cue in self.cues.values():
            yield (cue.name, cue.sample_offset)

    def label_and_note(self, cue_ident: int) -> Tuple[Optional[str],
                                                      Optional[str]]:
        """
        Get the label and note (extended comment) for a cue.

        :param cue_ident: the cue's name, its unique identifying number
        :returns: a tuple of the the cue's label (if present) and note (if
            present)
        """
        label = next((l for l in self.labels if l.name == cue_ident), None)
        note = next((n for n in self.notes if n.name == cue_ident), None)
        return (label.text if label else None, note.text if note else None)

    def range(self, cue_ident: int) -> Optional[int]:
        """
        Get the length of the time range for a cue, if it has one.

        :param cue_ident: the cue's name, its unique identifying number
        :returns: the length of the marker's range, or `None`
        """
        the_range = next((r for r in self.ranges if r.name == cue_ident), None)
        return the_range.length if the_range else None

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


class CueEntry(NamedTuple):
    """
    A ``cue`` element structure.
    """
    #: Cue "name" or id number
    name: int
    #: Cue position, as a frame count in the play order of the WAVE file. In
    #: principle this can be affected by playlists and ``wavl`` chunk
    #: placement.
    position: int
    chunk_id: bytes
    chunk_start: int
    block_start: int
    sample_offset: int


class LabelEntry(NamedTuple):
    """
    A ``labl`` structure.
    """
    name: int
    text: str


NoteEntry = LabelEntry


class RangeLabel(NamedTuple):
    """
    A ``ltxt`` structure.
    """
    name: int
    length: int
    purpose: str
    country: int
    language: int
    dialect: int
    codepage: int
    text: str
