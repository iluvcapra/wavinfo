[![Documentation Status](https://readthedocs.org/projects/wavinfo/badge/?version=latest)](https://wavinfo.readthedocs.io/en/latest/?badge=latest) ![](https://img.shields.io/github/license/iluvcapra/wavinfo.svg) ![](https://img.shields.io/pypi/pyversions/wavinfo.svg) [![](https://img.shields.io/pypi/v/wavinfo.svg)](https://pypi.org/project/wavinfo/) ![](https://img.shields.io/pypi/wheel/wavinfo.svg)
[![Lint and Test](https://github.com/iluvcapra/wavinfo/actions/workflows/python-package.yml/badge.svg)](https://github.com/iluvcapra/wavinfo/actions/workflows/python-package.yml)

# wavinfo

The `wavinfo` package allows you to probe WAVE and [RF64/WAVE files][eburf64] and extract extended metadata, with an emphasis on film, video and professional music production metadata.


## Metadata Support

`wavinfo` reads:

* [Broadcast-WAVE][bext] metadata, including embedded program
  loudness, coding history and [SMPTE UMID][smpte_330m2011].
* [ADM][adm] track metadata and schema, including channel, pack formats, object, content and programme.
* [Dolby Digital Plus][ebu3285s6] and Dolby Atmos `dbmd` metadata.
* [iXML][ixml] production recorder metadata, including project, scene, and take tags, recorder notes
  and file family information.
* Most of the common [RIFF INFO][info-tags] metadata fields.
* The __wav format__ is also parsed, so you can access the basic sample rate and channel count
  information.

In progress:
* Pro Tools __embedded regions__.
* iXML `STEINBERG` sound library attributes.

[bext]:https://wavinfo.readthedocs.io/en/latest/scopes/bext.html
[smpte_330m2011]:https://wavinfo.readthedocs.io/en/latest/scopes/bext.html#wavinfo.wave_bext_reader.WavBextReader.umid
[adm]:https://wavinfo.readthedocs.io/en/latest/scopes/adm.html
[ebu3285s6]:https://wavinfo.readthedocs.io/en/latest/scopes/dolby.html
[ixml]:https://wavinfo.readthedocs.io/en/latest/scopes/ixml.html
[info-tags]:https://wavinfo.readthedocs.io/en/latest/scopes/info.html
[eburf64]:https://tech.ebu.ch/docs/tech/tech3306v1_1.pdf


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
