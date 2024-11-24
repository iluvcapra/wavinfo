from unittest import TestCase
from glob import glob

import wavinfo

class TestSmpl(TestCase):
    def setUp(self) -> None:
        self.test_files = glob("tests/test_files/smpl/*.wav")
        return super().setUp()

    def test_each(self):
        for file in self.test_files:
            w = wavinfo.WavInfoReader(file)
            d = w.walk()
            self.assertIsNotNone(d)
