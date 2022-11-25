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


On Encodings
""""""""""""
According to Microsoft, the original developers of the RIFF file and RIFF INFO 
metadata, these fields are always to be interpreted as ISO Latin 1 characters, 
and this is the default encoding used by `wavinfo` for these fields. You can
select a different encoding (like Shift-JIS) by passing an encoding name (as 
would be used by `string.encode()`) to `WavInfoReader.__init__()`'s
`info_encoding=` parameter.
 


Class Reference
---------------

.. autoclass:: wavinfo.wave_info_reader.WavInfoChunkReader
   :members:




