INFO Metadata
=============

Notes
-----

INFO Metadata is a standard method for saving tagged text data in a WAV or AVI
file. INFO fields are often read by the file explorer and host OS, and used in 
music library software.


..  code:: python

    bullet_path = '../tests/test_files/BULLET Impact Plastic LCD TV Screen Shatter Debris 2x.wav'

    bullet = WavInfoReader(bullet_path)

    print("INFO Artist:",    bullet.info.artist)
    print("INFO Copyright:", bullet.info.copyright)
    print("INFO Comment:",   bullet.info.comment)


String Encoding of INFO Metadata
""""""""""""""""""""""""""""""""

Info metadata fields will be decoded using the string encoding passed to
:py:meth:`WavInfoReader's<wavinfo.wave_reader.WaveInfoReader.__init__>`
``info_encoding=`` parameter, which by default is ``latin_1`` (ISO 8859-1).

.. note::
   ``cset`` character set/locale metadata is not supported. If it is present
   in the file it will be ignored by `wavinfo`.

Class Reference
---------------

.. autoclass:: wavinfo.wave_info_reader.WavInfoChunkReader
   :members:




