"""
methods to probe a WAV file for various kinds of production metadata.

Go to the documentation for wavinfo.WavInfoReader for more information.
"""

from .wave_reader import WavInfoReader
from .riff_parser import WavInfoEOFError

__version__ = '1.6.3'
__author__ = 'Jamie Hardt <jamiehardt@gmail.com>'
__license__ = "MIT"
