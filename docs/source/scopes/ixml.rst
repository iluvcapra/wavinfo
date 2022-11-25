iXML Production Recorder Metadata
=================================

Notes
-----
iXML allows an XML document to be embedded in a WAV file.

The iXML website recommends a schema for recorder information but 
there is no official DTD and vendors mostly do their own thing, apart from 
hitting a few key xpaths. iXML is used by most location/production recorders 
to save slating information, timecode and sync points in a reliable way.

iXML is also used to link "families" of WAV files together, so WAV files
recorded simultaneously or contiguously can be related by a receiving client.

..  code:: python

    print("iXML Project:", info.ixml.project)
    print("iXML Scene:", info.ixml.scene)
    print("iXML Take:", info.ixml.take)
    print("iXML Tape:", info.ixml.tape)
    print("iXML File Family Name:", info.ixml.family_name)
    print("iXML File Family UID:", info.ixml.family_uid)

Result:

::

    iXML Project: BMH
    iXML Scene: A101
    iXML Take: 1
    iXML Tape: 18Y12M31
    iXML File Family Name: None
    iXML File Family UID: USSDVGR1112089007124001008206300


Class Reference
---------------

.. autoclass:: wavinfo.wave_ixml_reader.WavIXMLFormat
   :members:


