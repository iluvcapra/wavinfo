import unittest

from unittest.mock import patch

from wavinfo.__main__ import main

import sys

class MainTest(unittest.TestCase):
    
    def test_empty_argv(self): 
        with patch.object(sys, 'argv', []):
            try:
                main()
            except:
                self.fail("main() throwing an exception")

