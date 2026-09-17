# import os.path
import gzip
from glob import glob

# from typing import Dict, Any, cast
from unittest import TestCase

# from .utils import all_files, ffprobe
import wavinfo


class TestRf64(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_open(self):
        for path in glob("tests/test_files/rf64/*.wav.gz"):
            with gzip.open(path) as gz:
                wav_info = wavinfo.WavInfoReader(gz)
                self.assertIsNotNone(wav_info)
