wavinfo Quickstart
====================

All metadata is read by an instance of :class:`WaveInfoReader<wavinfo.wave_reader.WavInfoReader>`.
Each type of metadata, iXML, Broadcast-WAV etc. is accessible through *scopes*, properties on an 
instance of :class:`WaveInfoReader`. 


.. code-block:: python
    :caption: Using wavinfo

    import wavinfo

    path = 'path/to/your/wave/audio.wav'

    info = wavinfo.WavInfoReader(path)
    
    adm_metadata = info.adm
    ixml_metadata = info.ixml
    

.. module:: wavinfo
    :noindex:

.. autoclass:: wavinfo.wave_reader.WavInfoReader
   :members:

