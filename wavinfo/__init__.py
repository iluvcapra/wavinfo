"""
methods to probe a WAV file for various kinds of production metadata.

See the documentation for `wavinfo.WavInfoReader` for more information.
"""

from .wave_reader import WavInfoReader
from .riff_parser import WavInfoEOFError

__version__ = '2.1.0'
__author__ = 'Jamie Hardt <jamiehardt@gmail.com>'
__license__ = "MIT"
