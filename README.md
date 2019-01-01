[![Build Status](https://travis-ci.com/iluvcapra/wavinfo.svg?branch=master)](https://travis-ci.com/iluvcapra/wavinfo)
[![Documentation Status](https://readthedocs.org/projects/wavinfo/badge/?version=latest)](https://wavinfo.readthedocs.io/en/latest/?badge=latest) ![](https://img.shields.io/github/license/iluvcapra/wavinfo.svg) ![](https://img.shields.io/pypi/pyversions/wavinfo.svg) [![](https://img.shields.io/pypi/v/wavinfo.svg)](https://pypi.org/project/wavinfo/) ![](https://img.shields.io/pypi/wheel/wavinfo.svg)


# wavinfo


The `wavinfo` package allows you to probe WAVE files and extract extended metadata, with an emphasis on 
production metadata. 

`wavinfo` reads:

* __Broadcast-WAVE__ metadata, compliant with [EBU Tech 3285v2 (2011)][ebu], including embedded program loudness and coding history, if extant.
* [__iXML__ production recorder metadata][ixml], including project, scene, and take tags, recorder notes and file family information.
* The __wav format__ is also parsed, so you can access the basic sample rate and channel count information.

In progress:
* [SMPTE 330M __UMID__][smpte_330m2011] Unique Materials Identifier.
* iXML `STEINBERG` sound library attributes.
* Most of the common __RIFF INFO__ metadata fields.
* Pro Tools __embedded regions__.

This module is presently under construction and not sutiable for production at this time.

[ebu]:https://tech.ebu.ch/docs/tech/tech3285.pdf
[smpte_330m2011]:http://standards.smpte.org/content/978-1-61482-678-1/st-330-2011/SEC1.abstract
[ixml]:http://www.ixml.infoi



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

## Broadcast WAV Extension



```python
print(info.bext.description)
print("----------")
print("Originator:", info.bext.originator)
print("Originator Ref:", info.bext.originator_ref)
print("Originator Date:", info.bext.originator_date)
print("Originator Time:", info.bext.originator_time)
print("Time Reference:", info.bext.time_reference)
print(info.bext.coding_history)
```

    sSPEED=023.976-ND
    sTAKE=1
    sUBITS=$12311801
    sSWVER=2.67
    sPROJECT=BMH
    sSCENE=A101
    sFILENAME=A101_1.WAV
    sTAPE=18Y12M31
    sTRK1=MKH516 A
    sTRK2=Boom
    sNOTE=
    
    ----------
    Originator: Sound Dev: 702T S#GR1112089007
    Originator Ref: USSDVGR1112089007124001008206301
    Originator Date: 2018-12-31
    Originator Time: 12:40:00
    Time Reference: 2190940753
    A=PCM,F=48000,W=24,M=stereo,R=48000,T=2 Ch



## iXML Production Recorder Metadata


```python
print("iXML Project:", info.ixml.project)
print("iXML Scene:", info.ixml.scene)
print("iXML Take:", info.ixml.take)
print("iXML Tape:", info.ixml.tape)
print("iXML File Family Name:", info.ixml.family_name)
print("iXML File Family UID:", info.ixml.family_uid)
```

    iXML Project: BMH
    iXML Scene: A101
    iXML Take: 1
    iXML Tape: 18Y12M31
    iXML File Family Name: None
    iXML File Family UID: USSDVGR1112089007124001008206300
    


