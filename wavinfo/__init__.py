"""
Probe WAVE Files for iXML, Broadcast-WAVE and other metadata.
"""

from .reader.wave_reader import WavInfoReader
from .reader.riff_parser import WavInfoEOFError
from .writer.wave_writer import WavInfoWriter
from .session import WavInfo

__version__ = '3.0.0'
__short_version__ = '3.0.0'
