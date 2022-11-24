[![Documentation Status](https://readthedocs.org/projects/wavinfo/badge/?version=latest)](https://wavinfo.readthedocs.io/en/latest/?badge=latest) ![](https://img.shields.io/github/license/iluvcapra/wavinfo.svg) ![](https://img.shields.io/pypi/pyversions/wavinfo.svg) [![](https://img.shields.io/pypi/v/wavinfo.svg)](https://pypi.org/project/wavinfo/) ![](https://img.shields.io/pypi/wheel/wavinfo.svg)
[![Lint and Test](https://github.com/iluvcapra/wavinfo/actions/workflows/python-package.yml/badge.svg)](https://github.com/iluvcapra/wavinfo/actions/workflows/python-package.yml)

# wavinfo

The `wavinfo` package allows you to probe WAVE and [RF64/WAVE files][eburf64] and extract extended metadata, with an emphasis on film, video and professional music production metadata.


## Metadata Support

`wavinfo` reads:

* [__Broadcast-WAVE__][ebu] metadata, including embedded program
  loudness and coding history and [__SMPTE UMID__][smpte_330m2011].
* [__ADM__][adm] track metadata, including channel, pack formats, object and content names.
* [__iXML__][ixml] production recorder metadata, including project, scene, and take tags, recorder notes
  and file family information.
* Most of the common [__RIFF INFO__][info-tags] metadata fields.
* The __wav format__ is also parsed, so you can access the basic sample rate and channel count
  information.

In progress:
* [__Dolby RMU__][dolby] metadata and [EBU Tech 3285 Supplement 6][ebu3285s6].
* Pro Tools __embedded regions__.
* iXML `STEINBERG` sound library attributes.

[dolby]:https://developer.dolby.com/globalassets/documentation/technology/dolby_atmos_master_adm_profile_v1.0.pdf
[ebu]:https://tech.ebu.ch/docs/tech/tech3285.pdf
[ebu3285s6]:https://tech.ebu.ch/docs/tech/tech3285s6.pdf
[adm]:https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.2076-2-201910-I!!PDF-E.pdf
[smpte_330m2011]:http://standards.smpte.org/content/978-1-61482-678-1/st-330-2011/SEC1.abstract
[ixml]:http://www.ixml.info
[eburf64]:https://tech.ebu.ch/docs/tech/tech3306v1_1.pdf
[info-tags]:https://exiftool.org/TagNames/RIFF.html#Info

## How To Use

The entry point for wavinfo is the WavInfoReader class.

```python
from wavinfo import WavInfoReader

path = '../tests/test_files/A101_1.WAV'

info = WavInfoReader(path)

adm_metadata = info.adm
ixml_metadata = info.ixml
```

The package also installs a shell command:

```sh
$ wavinfo test_files/A101_1.WAV
```

## Other Resources

* For other file formats and ID3 decoding, look at [audio-metadata](https://github.com/thebigmunch/audio-metadata).
