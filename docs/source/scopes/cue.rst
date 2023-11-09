Cue Marker and Range Metadata
------------------------------

Notes
=====

Cue metadata stores timed markers that clients use to mark times of interest
in a wave file, and optionally give them a name and longer comment. Markers 
can also have an associated length, allowing ranges of times in a file to be 
marked.

String Encoding of Cue Metadata
"""""""""""""""""""""""""""""""

Cue labels and notes will be decoded using the string encoding passed to
:py:meth:`WavInfoReader's<wavinfo.wave_reader.WaveInfoReader.__init__>`
``info_encoding=`` parameter, which by default is ``latin_1`` (ISO 8859-1).

Text associated with ``ltxt`` time ranges may specify their own encoding in 
the form of a Windows codepage number. `wavinfo` will attempt to use the
encoding specified.

.. note::
   ``cset`` character set/locale metadata is not supported. If it is present
   in the file it will be ignored by `wavinfo`.

Class Reference
===============

.. autoclass:: wavinfo.wave_cues_reader.WavCuesReader
   :members:

.. autoclass:: wavinfo.wave_cues_reader.CueEntry
   :members:

.. autoclass:: wavinfo.wave_cues_reader.LabelEntry
   :members:

.. autoclass:: wavinfo.wave_cues_reader.NoteEntry
   :members:
