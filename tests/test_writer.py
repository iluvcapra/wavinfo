from io import SEEK_CUR, SEEK_SET, BytesIO
from struct import unpack
import unittest

from wavinfo import WavInfoWriter
from wavinfo.reader.riff_parser import ListChunkDescriptor, parse_chunk
from wavinfo.writer.list_writer import write_wave_file


class TestWriter(unittest.TestCase):

    def setUp(self):
        self.wave1 = BytesIO(bytes())

        with write_wave_file(self.wave1) as w:
            w.add_junk(1000)
            w.add_junk(500)
            w.add_child(b"data", b"\0" * 1024)
            w.add_junk(256)

        self.wave1.seek(0, SEEK_CUR)

        self.wave2 = BytesIO(bytes())

        with write_wave_file(self.wave2) as w:
            w.add_junk(500)
            with w.child_list(b"INFO") as info:
                info.add_child(b"IART", b"\0" * 32)
                info.add_child(b"ICMT", b"\0" * 144)
            w.add_child(b"data", b"\0" * 1000)

        self.wave2.seek(0, SEEK_CUR)


    def test_erase_chunk(self):
        w = WavInfoWriter(self.wave1)
        w.erase_chunk(b"data", 0)
        self.wave1.seek(12)
        self.assertEqual(b"JUNK", self.wave1.read(4))
        actual = unpack("<I", self.wave1.read(4))[0]
        self.assertEqual(actual, 2804)

    def test_erase_chunk_and_parse(self):
        w = WavInfoWriter(self.wave1)
        w.erase_chunk(b"data", 0)
        self.wave1.seek(0)
        ml = parse_chunk(self.wave1)
        assert type(ml) == ListChunkDescriptor
        self.assertEqual(len(ml.children), 1)

    def test_insert_chunk(self):
        w = WavInfoWriter(self.wave1)
        w.write_chunk(b"bext", b"\0".join([b"\0"] * 255), 
                      WavInfoWriter.Placement.FIRST_AVAILABLE)

    def test_erase_list(self):
        w = WavInfoWriter(self.wave2)
        w.erase_list_form(b"INFO", 0)
        self.wave2.seek(0, SEEK_SET)
        ml = parse_chunk(self.wave2)
        assert type(ml) == ListChunkDescriptor
        self.assertEqual(b"JUNK", ml.children[0].ident)
        self.assertEqual(152 + 40 + 4 + 8 + 500, ml.children[0].length)

        

