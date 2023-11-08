Broadcast WAV Extension Metadata
================================


Notes
-----
A WAV file produced to Broadcast-WAV specifications will have the broadcast
metadata extension, which includes a 256-character free text descrption,
creating entity identifier (usually the recording application or equipment),
the date and time of recording and a time reference for timecode
synchronization.

The :py:attr:`coding_history<wavinfo.wave_bext_reader.WavBextReader.coding_history>` 
is designed to contain a record of every conversion performed on the audio file.

In this example (from a Sound Devices 702T) the bext metadata contains
scene/take slating information in the
:py:attr:`description<wavinfo.wave_bext_reader.WavBextReader.description>`. 
Here also the
:py:attr:`originator_ref<wavinfo.wave_bext_reader.WavBextReader.originator_ref>`
is a serial number conforming to EBU Rec 99.

If the bext metadata conforms to `EBU 3285 v1`_, it will contain the WAV's 32
or 64 byte `SMPTE ST 330 UMID`_. The 32-byte version of the UMID is usually
just a random number, while the 64-byte UMID will also have information on the
recording date and time, recording equipment and entity, and geolocation data.

If the bext metadata conforms to `EBU 3285 v2`_, it will hold precomputed
program loudness values as described by `EBU Rec 128`_.

.. _EBU 3285 v1: https://tech.ebu.ch/publications/tech3285s1
.. _SMPTE ST 330 UMID: https://standards.globalspec.com/std/1396751/smpte-st-330
.. _EBU 3285 v2: https://tech.ebu.ch/publications/tech3285s2
.. _EBU Rec 128: https://tech.ebu.ch/publications/r128


.. note::
   All text fields in the Broadcast-WAV metadata structure are decoded by 
   default as flat ASCII. To override this and use a different encoding, pass
   an string encoding name to the ``bext_encoding`` parameter of
   :py:meth:`WavInfoReader()<wavinfo.wave_reader.WavInfoReader.__init__>`


Example
-------
..  code:: python

    print(info.bext.description)
    print("----------")
    print("Originator:", info.bext.originator)
    print("Originator Ref:", info.bext.originator_ref)
    print("Originator Date:", info.bext.originator_date)
    print("Originator Time:", info.bext.originator_time)
    print("Time Reference:", info.bext.time_reference)
    print(info.bext.coding_history)

Result: 

::

    sSPEED=023.976-ND
    sTAKE=1
    sUBITS=$12311801
    sSWVER=2.67
    sPROJECT=BMH
    sSCENE=A101
    sFILENAME=A101_1.WAV
    sTAPE=18Y12M31
    sTRK1=MKH516 A
    sTRK2=Boom
    sNOTE=
    
    ----------
    Originator: Sound Dev: 702T S#GR1112089007
    Originator Ref: USSDVGR1112089007124001008206301
    Originator Date: 2018-12-31
    Originator Time: 12:40:00
    Time Reference: 2190940753
    A=PCM,F=48000,W=24,M=stereo,R=48000,T=2 Ch


Class Reference
---------------

.. autoclass:: wavinfo.wave_bext_reader.WavBextReader
   :members:


