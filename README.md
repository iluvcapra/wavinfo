![](https://img.shields.io/pypi/pyversions/wavinfo.svg) [![](https://img.shields.io/pypi/v/wavinfo.svg)](https://pypi.org/project/wavinfo/) ![](https://img.shields.io/pypi/wheel/wavinfo.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/iluvcapra/wavinfo) [![Documentation Status](https://readthedocs.org/projects/wavinfo/badge/?version=latest)](https://wavinfo.readthedocs.io/en/latest/?badge=latest) ![](https://img.shields.io/github/license/iluvcapra/wavinfo.svg)

[![Tests](https://github.com/iluvcapra/wavinfo/actions/workflows/python-package.yml/badge.svg)](https://github.com/iluvcapra/wavinfo/actions/workflows/python-package.yml)
[![Flake8](https://github.com/iluvcapra/wavinfo/actions/workflows/python-flake8.yml/badge.svg)](https://github.com/iluvcapra/wavinfo/actions/workflows/python-flake8.yml)
[![codecov](https://codecov.io/gh/iluvcapra/wavinfo/branch/master/graph/badge.svg?token=9DZQfZENYv)](https://codecov.io/gh/iluvcapra/wavinfo)

# wavinfo

__See the [note below](#version-3-coming-soon) about version 3.__

The `wavinfo` package allows you to probe WAVE and [RF64/WAVE files][eburf64] 
and extract extended metadata. `wavinfo` has an emphasis on film, video and 
professional music production but can read many other kinds.

If you are trying to read a particular kind of metadata from a WAV file and
it is not supported, please submit an issue!


## Metadata Support

`wavinfo` reads:

* All defined [Broadcast-WAVE][bext] fields, including embedded program
  loudness, coding history and [SMPTE UMID][smpte_330m2011].
* [iXML][ixml] production recorder metadata, including project, scene, and 
  take tags, recorder notes and file family information.
  * iXML `STEINBERG` sound library attributes.
* All known [RIFF INFO][info-tags] metadata fields.
* [Audio Definition Model (ADM)][adm] track metadata and schema, including 
  channel, pack formats, 
  object, content and programme, including [Dolby Digital Plus][ebu3285s6]
  and Dolby Atmos `dbmd` metadata for re-renders and mixdowns.
* Wave embedded [cue markers][cues], cue marker labels, notes and timed ranges as used
  by Zoom, iZotope RX, etc.
* The [wav format][format] is also parsed, so you can access the basic sample rate 
  and channel count information.


[format]:https://wavinfo.readthedocs.io/en/latest/classes.html#wavinfo.wave_reader.WavAudioFormat
[cues]:https://wavinfo.readthedocs.io/en/latest/scopes/cue.html
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

## Version 3 Coming Soon!

Version 3 is under active development and will be released in the near future. 
Version 3 will support editing of Broadcast-WAVE and INFO metadata, 
with more formats to be added.

There will be some minor breaking changes with the interface which is why I'm
bumping to version 3, these will be documented and should be easy to update for.

## Contributions!

Any new or different kind of metadata you find, or any 
new or different use of exising metadata you encounter, please submit
an Issue or Pull Request!

## Other Resources

* For other file formats and ID3 decoding, 
  look at [audio-metadata](https://github.com/thebigmunch/audio-metadata).
