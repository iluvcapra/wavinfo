import glob
import sys
import unittest
from unittest.mock import patch

from wavinfo.__main__ import main


class MainTest(unittest.TestCase):
    def test_empty_argv(self):
        with patch.object(sys, "argv", []):
            try:
                main()
            except Exception as e:
                self.fail(f"main() throwing an exception: {e}")

    def test_a_file(self):
        for path in glob.glob("tests/test_files/**/*.wav"):
            with patch.object(sys, "argv", ["TEST", path]):
                try:
                    main()
                except Exception as e:
                    self.fail(f"main() throwing an exception: {e}")

    def test_ixml(self):
        with patch.object(
            sys, "argv", ["TEST", "--ixml", "tests/test_files/sounddevices/A101_1.WAV"]
        ):
            try:
                main()
            except Exception as e:
                self.fail(f"main() throwing an exception: {e}")
