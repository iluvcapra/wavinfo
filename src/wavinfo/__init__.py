"""
Probe WAVE Files for iXML, Broadcast-WAVE and other metadata.
"""

__all__ = ["WavInfoEOFError", "WavInfoReader"]

from .riff_parser import WavInfoEOFError
from .wave_reader import WavInfoReader
