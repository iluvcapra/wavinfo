[![Build Status](https://travis-ci.com/iluvcapra/wavinfo.svg?branch=master)](https://travis-ci.com/iluvcapra/wavinfo)
[![Documentation Status](https://readthedocs.org/projects/wavinfo/badge/?version=latest)](https://wavinfo.readthedocs.io/en/latest/?badge=latest) ![](https://img.shields.io/github/license/iluvcapra/wavinfo.svg) ![](https://img.shields.io/pypi/pyversions/wavinfo.svg) [![](https://img.shields.io/pypi/v/wavinfo.svg)](https://pypi.org/project/wavinfo/) ![](https://img.shields.io/pypi/wheel/wavinfo.svg)


# wavinfo


The `wavinfo` package allows you to probe WAVE and [RF64/WAVE files][eburf64] and extract extended metadata, with an emphasis on film, video and professional music production metadata. 

`wavinfo` reads:

* __Broadcast-WAVE__ metadata, compliant with [EBU Tech 3285v2 (2011)][ebu], including embedded program 
  loudness and coding history, if extant. This also includes the [SMPTE 330M __UMID__][smpte_330m2011] 
  Unique Materials Identifier.
* [__iXML__ production recorder metadata][ixml], including project, scene, and take tags, recorder notes 
  and file family information.
* Most of the common __RIFF INFO__ metadata fields.
* The __wav format__ is also parsed, so you can access the basic sample rate and channel count 
  information.

In progress:
* iXML `STEINBERG` sound library attributes.
* Pro Tools __embedded regions__.

[ebu]:https://tech.ebu.ch/docs/tech/tech3285.pdf
[smpte_330m2011]:http://standards.smpte.org/content/978-1-61482-678-1/st-330-2011/SEC1.abstract
[ixml]:http://www.ixml.info
[eburf64]:https://tech.ebu.ch/docs/tech/tech3306v1_1.pdf



## Demonstration

The entry point for wavinfo is the WavInfoReader class.

```python
from wavinfo import WavInfoReader

path = '../tests/test_files/A101_1.WAV'

info = WavInfoReader(path)
```

### Basic WAV Data

The length of the file in frames (interleaved samples) and bytes is available, as is the contents of the format chunk.

```python
(info.data.frame_count, info.data.byte_count)
>>> (240239, 1441434)
(info.fmt.sample_rate, info.fmt.channel_count, info.fmt.block_align, info.fmt.bits_per_sample)
>>> (48000, 2, 6, 24)
```

## Other Resources

* For other file formats and ID3 decoding, look at [audio-metadata](https://github.com/thebigmunch/audio-metadata).




