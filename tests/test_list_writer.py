from io import SEEK_SET, BytesIO
from logging import info
import unittest

from wavinfo.writer.list_writer import write_wave_file
from wavinfo.reader.riff_parser import ChunkDescriptor, ListChunkDescriptor, parse_chunk

class TestListWriter(unittest.TestCase):

    def setUp(self):
        self.backing = bytes()
        self.buffer = BytesIO(self.backing)

        with write_wave_file(self.buffer) as t:
            t.add_junk(1024)
            t.add_child(b"fmt ", b"\0" * 64)
            with t.child_list(b"INFO") as info:
                info.add_child(b"IART", b"Test 1 2 3")
                info.add_child(b"ICMT", b"This is a free text comment")

            t.add_child(b"data", b"\0" * 1024)

        self.buffer.seek(0, SEEK_SET)

    def test_wave_list(self):
        ml = parse_chunk(self.buffer)
        assert type(ml) == ListChunkDescriptor
        self.assertEqual(len(ml.children), 4)

        assert type(ml.children[0]) == ChunkDescriptor
        self.assertEqual(ml.children[0].ident, b"JUNK")
        self.assertEqual(ml.children[0].length, 1024)
       
        assert type(ml.children[1]) == ChunkDescriptor
        self.assertEqual(ml.children[1].ident, b"fmt ")
        self.assertEqual(ml.children[1].length, 64)

        assert type(ml.children[2]) == ListChunkDescriptor

        assert type(ml.children[3]) == ChunkDescriptor
        self.assertEqual(ml.children[3].ident, b"data")
        self.assertEqual(ml.children[3].length, 1024)

    def test_child_list(self):
        ml = parse_chunk(self.buffer)     
        assert type(ml) == ListChunkDescriptor
        assert type(ml.children[2]) == ListChunkDescriptor
        info_list = ml.children[2]
        self.assertEqual(info_list.ident, b"LIST")
        self.assertEqual(info_list.signature, b"INFO")
        self.assertEqual(len(info_list.children), 2)

        assert type(info_list.children[0]) == ChunkDescriptor
        self.assertEqual(info_list.children[0].ident, b"IART")
        self.assertEqual(info_list.children[0].length, 10)
        
        assert type(info_list.children[1] == ChunkDescriptor)
        self.assertEqual(info_list.children[1].ident, b"ICMT")
        self.assertEqual(info_list.children[1].length, 27)

        
