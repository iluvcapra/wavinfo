import os.path
import json
import subprocess

from unittest import TestCase

import wavinfo

FFPROBE='/usr/local/bin/ffprobe'


def ffprobe(path):

    arguments = [ FFPROBE , "-of", "json" , "-show_format", "-show_streams", path ]

    process = subprocess.run(arguments, stdin=None, capture_output=True)

    if process.returncode == 0:
        return json.loads(process.stdout)
    else:
        return None


class TestWaveInfo(TestCase):


    def all_files(self):
        for dirpath, dirnames, filenames in os.walk('tests/test_files'):
            for filename in filenames:
                name, ext = os.path.splitext(filename)
                if ext == '.wav':
                    yield os.path.join(dirpath, filename)


    def test_sanity(self):
        for wav_file in self.all_files():
            info = wavinfo.WavInfoReader(wav_file)
            self.assertTrue(info is not None)

    def test_fmt_against_ffprobe(self):
        for wav_file in self.all_files():
            info = wavinfo.WavInfoReader(wav_file)
            ffprobe_info = ffprobe(wav_file)

            self.assertEqual( info.fmt.channel_count , ffprobe_info['streams'][0]['channels']  )
            self.assertEqual( info.fmt.sample_rate   , int(ffprobe_info['streams'][0]['sample_rate'])  )
            self.assertEqual( info.fmt.bits_per_sample, int(ffprobe_info['streams'][0]['bits_per_raw_sample']) )

            if info.fmt.audio_format == 1:
                self.assertTrue(ffprobe_info['streams'][0]['codec_name'].startswith('pcm')  )
                byte_rate = int(ffprobe_info['streams'][0]['sample_rate']) \
                        * ffprobe_info['streams'][0]['channels'] \
                        * int(ffprobe_info['streams'][0]['bits_per_raw_sample']) / 8
                self.assertEqual( info.fmt.byte_rate     , byte_rate  )

    def test_data_against_ffprobe(self):
        for wav_file in self.all_files():
            info = wavinfo.WavInfoReader(wav_file)
            ffprobe_info = ffprobe(wav_file)

            self.assertEqual( info.data.frame_count, int(ffprobe_info['streams'][0]['duration_ts'] ))

    def test_bext_against_ffprobe(self):
        for wav_file in self.all_files():
            info = wavinfo.WavInfoReader(wav_file)
            ffprobe_info = ffprobe(wav_file)

            self.assertEqual( info.bext.description, ffprobe_info['format']['tags']['comment']  )
            self.assertEqual( info.bext.originator, ffprobe_info['format']['tags']['encoded_by']  )
            self.assertEqual( info.bext.originator_ref, ffprobe_info['format']['tags']['originator_reference']  )

            # these don't always reflect the bext info
            #self.assertEqual( info.bext.originator_date, ffprobe_info['format']['tags']['date']  )
            #self.assertEqual( info.bext.originator_time, ffprobe_info['format']['tags']['creation_time']  )
            self.assertEqual( info.bext.time_reference, int(ffprobe_info['format']['tags']['time_reference'])  )
            self.assertEqual( info.bext.coding_history, ffprobe_info['format']['tags']['coding_history']  )

    def test_ixml(self):
        expected = {'A101_4.WAV': {'project' : 'BMH', 'scene': 'A101', 'take': '4',
                        'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124015008231000'},
                    'A101_3.WAV': {'project' : 'BMH', 'scene': 'A101', 'take': '3',
                        'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124014008228300'},
                    'A101_2.WAV': {'project' : 'BMH', 'scene': 'A101', 'take': '2',
                        'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124004008218600'},
                    'A101_1.WAV': {'project' : 'BMH', 'scene': 'A101', 'take': '1',
                        'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124001008206300'},
                }

        for wav_file in self.all_files():
            basename =  os.path.basename(wav_file)
            if basename in expected:
                info = wavinfo.WavInfoReader(wav_file)
                e = expected[basename]

                self.assertEqual( e['project'], info.ixml.project )
                self.assertEqual( e['scene'], info.ixml.scene )
                self.assertEqual( e['take'], info.ixml.take )
                self.assertEqual( e['tape'], info.ixml.tape )
                self.assertEqual( e['family_uid'], info.ixml.family_uid )
