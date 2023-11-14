from io import SEEK_CUR, SEEK_SET, BytesIO
from struct import pack, unpack
import unittest

from wavinfo import WavInfoWriter
from wavinfo.reader.riff_parser import ListChunkDescriptor, parse_chunk

class TestWriter(unittest.TestCase):

    def setUp(self):
        wavelist = b"WAVE" + b"JUNK" + pack("<I1000x", 1000)
        wavelist += b"JUNK" + pack("<I500x", 500)
        wavelist += b"data" + pack("<I1024x", 1024)
        wavelist += b"JUNK" + pack("<I256x", 256)
        self.buffer1 = b"RIFF" + pack("<I", len(wavelist)) + wavelist

    def test_combine_junk(self):
        f = BytesIO(self.buffer1)
        w = WavInfoWriter(f, preserve_ds64_reservation=False)
        w._combine_adjacent_junk()
        self.assertEqual(self.buffer1[12:16], b"JUNK")
        f.seek(16)
        actual_size = unpack("<I", f.read(4))[0]
        self.assertEqual(actual_size, 1508)

    def test_split_junk(self):
        f = BytesIO(self.buffer1)
        w = WavInfoWriter(f, preserve_ds64_reservation=False)
        self.assertTrue(w._can_split_junk(0, 500))
        self.assertFalse(w._can_split_junk(1, 496))
        self.assertFalse(w._can_split_junk(1, 492))
        self.assertFalse(w._can_split_junk(1, 491))
        self.assertTrue(w._can_split_junk(1, 490))
        w._split_junk(0, 500)
        f.seek(16, SEEK_SET)
        actual_size_a = unpack("<I", f.read(4))[0]
        self.assertTrue(actual_size_a, 500)
        f.seek(500, SEEK_CUR)
        self.assertEqual(b"JUNK", f.read(4))
        actual_size_b = unpack("<I", f.read(4))[0]
        self.assertEqual(actual_size_b, 492)

    def test_erase_chunk(self):
        f = BytesIO(self.buffer1)
        w = WavInfoWriter(f, preserve_ds64_reservation=False)
        w.erase_chunk(b"data", 0)
        f.seek(12)
        self.assertEqual(b"JUNK", f.read(4))
        actual = unpack("<I", f.read(4))[0]
        self.assertEqual(actual, 2804)

    def test_erase_chunk_and_parse(self):
        f = BytesIO(self.buffer1)
        w = WavInfoWriter(f, preserve_ds64_reservation=False)
        w.erase_chunk(b"data", 0)
        f.seek(0)
        ml = parse_chunk(f)
        assert type(ml) == ListChunkDescriptor
        self.assertEqual(len(ml.children), 1)

    def test_insert_chunk(self):
        f = BytesIO(self.buffer1)
        w = WavInfoWriter(f, preserve_ds64_reservation=False)
        w.write_chunk(b"bext", b"\0".join([b"\0"] * 255), 
                      WavInfoWriter.Placement.FIRST_AVAILABLE)
        

