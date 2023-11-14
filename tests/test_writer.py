from io import SEEK_CUR, SEEK_SET, BytesIO
from struct import unpack
import unittest

from wavinfo import WavInfoWriter
from wavinfo.reader.riff_parser import ChunkDescriptor, ListChunkDescriptor, parse_chunk
from wavinfo.writer.list_writer import write_wave_file


class TestWriter(unittest.TestCase):

    def assert_lists_equal(self, made_list: ListChunkDescriptor,
                           expected_list: ListChunkDescriptor):

        self.assertEqual(made_list.length, expected_list.length)

        self.assertEqual(len(made_list.children), len(expected_list.children))

        for i, (mc, ec) in enumerate(
                zip(made_list.children, expected_list.children)):
            self.assertEqual(mc.length, ec.length, f"Length of child chunk "
                             "{i} does not match")
            self.assertEqual(mc.start, ec.start, f"Start of child chunk {i} "
                             "does not match")
            self.assertEqual(mc.ident, ec.ident)
            self.assertEqual(type(mc), type(ec))
            assert isinstance(mc, ChunkDescriptor)
            assert isinstance(ec, ChunkDescriptor)

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

    def test_erase_chunk_and_parse(self):
        w = WavInfoWriter(self.wave1)
        w.erase_chunk(b"data", 0)
        self.wave1.seek(0)
        ml = parse_chunk(self.wave1)
        # breakpoint()
        assert isinstance(ml, ListChunkDescriptor)
        self.assertEqual(len(ml.children), 0)

    def test_insert_chunk(self):
        w = WavInfoWriter(self.wave1)
        w.write_chunk(b"bext", b"\0" * 255,
                      WavInfoWriter.Placement.FIRST_AVAILABLE)

        # breakpoint()
        expected = BytesIO(bytes())

        with write_wave_file(expected) as e:
            e.add_child(b"bext", b"\0" * 255)
            e.add_junk(1244)
            e.add_child(b"data", b"\0" * 1024)

        self.wave1.seek(0, SEEK_SET)
        expected.seek(0, SEEK_SET)

        (made_list, expected_list) = (parse_chunk(self.wave1),
                                      parse_chunk(expected))

        assert isinstance(made_list, ListChunkDescriptor)
        assert isinstance(expected_list, ListChunkDescriptor)
        self.assert_lists_equal(made_list, expected_list)

    def test_erase_list(self):
        w = WavInfoWriter(self.wave2)
        w.erase_list_form(b"INFO", 0)
        self.wave2.seek(0, SEEK_SET)
        ml = parse_chunk(self.wave2)
        assert isinstance(ml, ListChunkDescriptor)
        self.assertEqual(b"JUNK", ml.children[0].ident)
        self.assertEqual(152 + 40 + 4 + 8 + 500, ml.children[0].length)
