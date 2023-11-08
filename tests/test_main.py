import unittest

from unittest.mock import patch

from wavinfo.__main__ import main

import sys
import glob

class MainTest(unittest.TestCase):
    
    def test_empty_argv(self): 
        with patch.object(sys, 'argv', []):
            try:
                main()
            except:
                self.fail("main() throwing an exception")

    def test_a_file(self):
        for path in glob.glob("tests/test_files/**/*.wav"):
            with patch.object(sys, 'argv', [path]):
                try:
                    main()
                except:
                    self.fail("main() throwing an exception") 

    def test_ixml(self):
        with patch.object(sys, 'argv', 
                          ['tests/test_files/sounddevices/A101_1.WAV']):
            try:
                main()
            except:
                self.fail("main() throwing an exception") 
