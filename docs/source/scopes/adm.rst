ADM (Audio Definition Model) Metadata
=====================================

Notes
-----

`ADM metadata`_ is used in master recordings to describe the format and content 
of the tracks. In practice on wave files, ADM tells a client which tracks are 
members of multichannel stems or "beds" and their speaker assignment, and which 
tracks are freely-positioned 3D objects. ADM also records the panning moves on
object tracks and their content group ("Dialogue", "Music", "Effects" etc.)

ADM wave files created with a Dolby Rendering and Mastering Unit are a common 
deliverable in feature film and television production. The `Dolby Atmos ADM Profile`_ 
describes how the RMU translates its native Master format into ADM. 
 

.. _ADM metadata: https://adm.ebu.io
.. _Dolby Atmos ADM Profile: https://developer.dolby.com/globalassets/documentation/technology/dolby_atmos_master_adm_profile_v1.0.pdf

Class Reference
---------------

.. module:: wavinfo

.. autoclass:: wavinfo.wave_adm_reader.WavADMReader
    :members:

.. autoclass:: wavinfo.wave_adm_reader.ChannelEntry
    :members: