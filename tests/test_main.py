import glob
import sys
import unittest
from unittest.mock import patch

from wavinfo.__main__ import main


class MainTest(unittest.TestCase):
    def test_empty_argv(self):
        with patch.object(sys, "argv", []):
            main()

    def test_a_file(self):
        for path in glob.glob("tests/test_files/**/*.wav"):
            with patch.object(sys, "argv", ["TEST", path]):
                 main()

    def test_ixml(self):
        with patch.object(
            sys, "argv", ["TEST", "--ixml", "tests/test_files/sounddevices/A101_1.WAV"]
        ):
            main()
