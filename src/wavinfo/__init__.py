"""
Probe WAVE Files for iXML, Broadcast-WAVE and other metadata.
"""

__all__ = ['WavInfoReader', 'WavInfoEOFError']

from .wave_reader import WavInfoReader
from .riff_parser import WavInfoEOFError

