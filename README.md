[![Build Status](https://travis-ci.com/iluvcapra/wavinfo.svg?branch=master)](https://travis-ci.com/iluvcapra/wavinfo)
[![Coverage Status](https://coveralls.io/repos/github/iluvcapra/wavinfo/badge.svg?branch=master)](https://coveralls.io/github/iluvcapra/wavinfo?branch=master)
[![Documentation Status](https://readthedocs.org/projects/wavinfo/badge/?version=latest)](https://wavinfo.readthedocs.io/en/latest/?badge=latest) ![](https://img.shields.io/github/license/iluvcapra/wavinfo.svg) ![](https://img.shields.io/pypi/pyversions/wavinfo.svg) [![](https://img.shields.io/pypi/v/wavinfo.svg)](https://pypi.org/project/wavinfo/) ![](https://img.shields.io/pypi/wheel/wavinfo.svg)


# wavinfo


The `wavinfo` package allows you to probe WAVE files and extract extended metadata, with an emphasis on 
production metadata. 

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

### Broadcast WAV Extension

A WAV file produced to Broadcast-WAV specifications will have the broadcast metadata extension,
which includes a 256-character free text descrption, creating entity identifier (usually the 
recording application or equipment), the date and time of recording and a time reference for 
timecode synchronization.

The `coding_history` is designed to contain a record of every conversion performed on the audio
file.

In this example (from a Sound Devices 702T) the bext metadata contains scene/take slating
information in the `description`. Here also the `originator_ref` is a serial number conforming
to EBU Rec 99.

If the bext metadata conforms to EBU 3285 v1, it will contain the WAV's 32 or 64 byte SMPTE 
330M UMID. The 32-byte version of the UMID is usually just a random number, while the 64-byte 
UMID will also have information on the recording date and time, recording equipment and entity, 
and geolocation data.

If the bext metadata conforms to EBU 3285 v2, it will hold precomputed program loudness values
as described by EBU Rec 128.

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



### iXML Production Recorder Metadata

iXML allows an XML document to be embedded in a WAV file.

The iXML website recommends a schema for recorder information but 
there is no official DTD and vendors mostly do their own thing, apart from 
hitting a few key xpaths. iXML is used by most location/production recorders 
to save slating information, timecode and sync points in a reliable way.

iXML is also used to link "families" of WAV files together, so WAV files
recorded simultaneously or contiguously can be related by a receiving client.

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


### INFO Metadata

INFO Metadata is a standard method for saving tagged text data in a WAV or AVI
file. INFO fields are often read by the file explorer and host OS, and used in 
music library software.

```python
bullet_path = '../tests/test_files/BULLET Impact Plastic LCD TV Screen Shatter Debris 2x.wav'

bullet = WavInfoReader(bullet_path)
```

    print("INFO Artist:",    bullet.info.artist)
    print("INFO Copyright:", bullet.info.copyright)
    print("INFO Comment:",   bullet.info.comment)


