Using `wavinfo` from the Command Line
=====================================

`wavinfo` installs a command-line entry point that will read wav files
from the command line and output metadata to stdout.

.. code-block:: shell

    $ wavinfo [[-i] | [--ixml | --adm]] INFILE +


Options
-------

By default, `wavinfo` will output a JSON dictionary for each file argument.

``-i`` 
    `wavinfo` will run in `interactive mode`_.

Two option flags will change the behavior of the command in non-interactive 
mode:

``--ixml``
    The *\-\-ixml* flag will cause `wavinfo` to output the iXML metadata
    payload of each input wave file, or will emit an error message to stderr if
    iXML metadata is not present.

``--adm``
    The *\-\-adm* flag will cause `wavinfo` to output the ADM XML metadata 
    payload of each input wave file, or will emit an error message to stderr if
    ADM XML metadata is not present.

These options are mutually-exclusive, with `\-\-adm` taking precedence. The 
``--ixml`` and ``--adm`` flags futher take precedence over ``-i``.


Interactive Mode 
-----------------

In interactive mode, `wavinfo` will present a command prompt which allows you
to query the files provided on the command line and explore the metadata tree 
interactively. Each file on the command line is scanned and presented as a 
tree of metadata records.

Commands include:

``ls``
    List the available metadata keys at the current level.

``cd``
    Traverse to a metadata key in the current level (or enter `..` to go up 
    to the prevvious level).

``bye``
    Exit to the shell.

Type `help` or `?` at the prompt to get a full list of commands.


Example Output
--------------

.. code-block:: javascript

    {
    "filename": "tests/test_files/sounddevices/A101_1.WAV",
    "run_date": "2022-11-26T17:56:38.342935",
    "application": "wavinfo 2.1.0",
    "scopes": {
        "fmt": {
        "audio_format": 1,
        "channel_count": 2,
        "sample_rate": 48000,
        "byte_rate": 288000,
        "block_align": 6,
        "bits_per_sample": 24
        },
        "data": {
        "byte_count": 1441434,
        "frame_count": 240239
        },
        "ixml": {
        "track_list": [
            {
            "channel_index": "1",
            "interleave_index": "1",
            "name": "MKH516 A",
            "function": ""
            },
            {
            "channel_index": "2",
            "interleave_index": "2",
            "name": "Boom",
            "function": ""
            }
        ],
        "project": "BMH",
        "scene": "A101",
        "take": "1",
        "tape": "18Y12M31",
        "family_uid": "USSDVGR1112089007124001008206300",
        "family_name": null
        },
        "bext": {
        "description": "sSPEED=023.976-ND\r\nsTAKE=1\r\nsUBITS=$12311801\r\nsSWVER=2.67\r\nsPROJECT=BMH\r\nsSCENE=A101\r\nsFILENAME=A101_1.WAV\r\nsTAPE=18Y12M31\r\nsTRK1=MKH516 A\r\nsTRK2=Boom\r\nsNOTE=\r\n",
        "originator": "Sound Dev: 702T S#GR1112089007",
        "originator_ref": "USSDVGR1112089007124001008206301",
        "originator_date": "2018-12-31",
        "originator_time": "12:40:00",
        "time_reference": 2190940753,
        "version": 1,
        "umid": "0000000000000000000000000000000000000000000000000000000000000000",
        "coding_history": "A=PCM,F=48000,W=24,M=stereo,R=48000,T=2 Ch\r\n",
        "loudness_value": null,
        "loudness_range": null,
        "max_true_peak": null,
        "max_momentary_loudness": null,
        "max_shortterm_loudness": null
        }
    }
    }

