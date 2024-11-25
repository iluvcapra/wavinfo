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

.. attention::

   Metadata fields containing binary data, such as the Broadcast-WAV UMID, will 
   be included in the JSON output as a base-64 encoded string, preceded by the
   marker "base64:".

.. code-block:: javascript

  {
  "filename": "../tests/test_files/nuendo/wavinfo Test Project - Audio - 1OA.wav",
  "run_date": "2024-11-25T10:26:11.280053",
  "application": "wavinfo 3.0.0",
  "scopes": {
    "fmt": {
      "audio_format": 65534,
      "channel_count": 4,
      "sample_rate": 48000,
      "byte_rate": 576000,
      "block_align": 12,
      "bits_per_sample": 24
    },
    "data": {
      "byte_count": 576000,
      "frame_count": 48000
    },
    "ixml": {
      "track_list": [
        {
          "channel_index": "1",
          "interleave_index": "1",
          "name": "",
          "function": "ACN0-FOA"
        },
        {
          "channel_index": "2",
          "interleave_index": "2",
          "name": "",
          "function": "ACN1-FOA"
        },
        {
          "channel_index": "3",
          "interleave_index": "3",
          "name": "",
          "function": "ACN2-FOA"
        },
        {
          "channel_index": "4",
          "interleave_index": "4",
          "name": "",
          "function": "ACN3-FOA"
        }
      ],
      "project": "wavinfo Test Project",
      "scene": null,
      "take": null,
      "tape": null,
      "family_uid": "E5DDE719B9484A758162FF7B652383A3",
      "family_name": null
    },
    "bext": {
      "description": "wavinfo Test Project Nuendo output",
      "originator": "Nuendo",
      "originator_ref": "USJPHNNNNNNNNN202829RRRRRRRRR",
      "originator_date": "2022-12-02",
      "originator_time": "10:21:06",
      "time_reference": 172800000,
      "version": 2,
      "umid": "base64:k/zr4qE4RiaXyd/fO7GuCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==",
      "coding_history": "A=PCM,F=48000,W=24,T=Nuendo\r\n",
      "loudness_value": 327.67,
      "loudness_range": 327.67,
      "max_true_peak": 327.67,
      "max_momentary_loudness": 327.67,
      "max_shortterm_loudness": 327.67
    }
  }
}

