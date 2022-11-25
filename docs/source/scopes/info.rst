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


Class Reference
---------------

.. autoclass:: wavinfo.wave_info_reader.WavInfoChunkReader
   :members:




