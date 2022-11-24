
wavinfo
=======

The `wavinfo` package allows you to probe WAVE and `RF64/WAVE files<ebu3306>`_ 
and extract extended metadata, with an emphasis on film, video and professional
music production metadata.

Metadata Standard Support
-------------------------

`wavinfo` reads:

* `__Broadcast-WAVE__<ebu_bwf>` metadata, including embedded program
  loudness and coding history, and `SMPTE UMID<smpte_330m2011>`.
* `__ADM__<adm>` track metadata<sup>[3][adm]</sup>, including channel, pack formats, object and content names.
* `__iXML__<ixml>` production recorder metadata<sup>[4][ixml]</sup>, including project, scene, and take tags, recorder notes
  and file family information.
* Most of the common `__RIFF_INFO__<info-tags>` metadata fields.
* The __wav_format__ is also parsed, so you can access the basic sample rate and channel count
  information.

In progress:

* [Dolby RMU][dolby] metadata and [EBU Tech 3285 Supplement 6][ebu3285s6].
* iXML `STEINBERG` sound library attributes.
* __NetMix__ library attributes.
* Pro Tools __embedded_regions__.

How To Use
----------

Check out the quick start, but using `wavinfo` is very simple.

.. code-block:: python
  :caption: Reading metadata
  from wavinfo import WavInfoReader

  path = '../tests/test_files/A101_1.WAV'

  metadata = WavInfoReader(path)


Installation
------------

The best way to install `wavinfo` is thew `pypi`:

.. code-block:: shell
  $ pip3 install wavinfo




.. _ebu3306: https://tech.ebu.ch/docs/tech/tech3306v1_1.pdf
.. _smpte_330m2011: http://standards.smpte.org/content/978-1-61482-678-1/st-330-2011/SEC1.abstract
.. _ebu_bwf: https://tech.ebu.ch/docs/tech/tech3285.pdf
.. _adm: https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.2076-2-201910-I!!PDF-E.pdf
.. _ixml: http://www.ixml.info
.. _info-tags: https://exiftool.org/TagNames/RIFF.html#Info

