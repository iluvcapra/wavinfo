import os.path

from unittest import TestCase

from .utils import all_files, ffprobe

import wavinfo


class TestWaveInfo(TestCase):
    def test_sanity(self):
        for wav_file in all_files():
            info = wavinfo.WavInfoReader(wav_file)
            self.assertEqual(info.__repr__(), 'WavInfoReader({}, latin_1, ascii)'.format(os.path.abspath(wav_file)))
            self.assertIsNotNone(info)

    def test_fmt_against_ffprobe(self):
        for wav_file in all_files():
            info = wavinfo.WavInfoReader(wav_file)
            ffprobe_info = ffprobe(wav_file)

            self.assertEqual(info.fmt.channel_count, ffprobe_info['streams'][0]['channels'])
            self.assertEqual(info.fmt.sample_rate, int(ffprobe_info['streams'][0]['sample_rate']))
            self.assertEqual(info.fmt.bits_per_sample, int(ffprobe_info['streams'][0]['bits_per_raw_sample']))

            if info.fmt.audio_format == 1:
                self.assertTrue(ffprobe_info['streams'][0]['codec_name'].startswith('pcm'))
                streams = ffprobe_info['streams'][0]
                byte_rate = int(streams['sample_rate']) * streams['channels'] * int(streams['bits_per_raw_sample']) / 8
                self.assertEqual(info.fmt.byte_rate, byte_rate)

    def test_data_against_ffprobe(self):
        for wav_file in all_files():
            info = wavinfo.WavInfoReader(wav_file)
            ffprobe_info = ffprobe(wav_file)
            self.assertEqual(info.data.frame_count, int(ffprobe_info['streams'][0]['duration_ts']))

    def test_bext_against_ffprobe(self):
        for wav_file in all_files():
            info = wavinfo.WavInfoReader(wav_file)
            ffprobe_info = ffprobe(wav_file)
            if info.bext:
                if 'comment' in ffprobe_info['format']['tags']:
                    self.assertEqual(info.bext.description, ffprobe_info['format']['tags']['comment'])
                else:
                    self.assertEqual(info.bext.description, '')

                if 'encoded_by' in ffprobe_info['format']['tags']:
                    self.assertEqual(info.bext.originator, ffprobe_info['format']['tags']['encoded_by'])
                else:
                    self.assertEqual(info.bext.originator, '')

                if 'originator_reference' in ffprobe_info['format']['tags']:
                    self.assertEqual(info.bext.originator_ref, ffprobe_info['format']['tags']['originator_reference'])
                else:
                    self.assertEqual(info.bext.originator_ref, '')

                # these don't always reflect the bext info
                # self.assertEqual(info.bext.originator_date, ffprobe_info['format']['tags']['date'])
                # self.assertEqual(info.bext.originator_time, ffprobe_info['format']['tags']['creation_time'])
                self.assertEqual(info.bext.time_reference, int(ffprobe_info['format']['tags']['time_reference']))

                if 'coding_history' in ffprobe_info['format']['tags']:
                    self.assertEqual(info.bext.coding_history, ffprobe_info['format']['tags']['coding_history'])
                else:
                    self.assertEqual(info.bext.coding_history, '')

    def test_ixml(self):
        expected = {'A101_4.WAV': {'project': 'BMH', 'scene': 'A101', 'take': '4',
                                   'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124015008231000'},
                    'A101_3.WAV': {'project': 'BMH', 'scene': 'A101', 'take': '3',
                                   'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124014008228300'},
                    'A101_2.WAV': {'project': 'BMH', 'scene': 'A101', 'take': '2',
                                   'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124004008218600'},
                    'A101_1.WAV': {'project': 'BMH', 'scene': 'A101', 'take': '1',
                                   'tape': '18Y12M31', 'family_uid': 'USSDVGR1112089007124001008206300'},
                    }

        for wav_file in all_files():
            basename = os.path.basename(wav_file)
            if basename in expected:
                info = wavinfo.WavInfoReader(wav_file)
                e = expected[basename]

                self.assertEqual(e['project'], info.ixml.project)
                self.assertEqual(e['scene'], info.ixml.scene)
                self.assertEqual(e['take'], info.ixml.take)
                self.assertEqual(e['tape'], info.ixml.tape)
                self.assertEqual(e['family_uid'], info.ixml.family_uid)

                for track in info.ixml.track_list:
                    self.assertIsNotNone(track.channel_index)
                    if basename == 'A101_4.WAV' and track.channel_index == '1':
                        self.assertEqual(track.name, 'MKH516 A')

    def test_metadata(self):
        file_with_metadata = 'tests/test_files/sound_grinder_pro/new_camera bumb 1.wav'
        self.assertTrue(os.path.exists(file_with_metadata))
        info = wavinfo.WavInfoReader(file_with_metadata).info
        self.assertEqual(info.title, 'camera bumb 1')
        self.assertEqual(info.artist, 'Jamie Hardt')
        self.assertEqual(info.copyright, 'Â© 2010 Jamie Hardt')
        self.assertEqual(info.product, 'Test Sounds')  # album
        self.assertEqual(info.album, info.product)
        self.assertEqual(info.comment, 'Comments')
        self.assertEqual(info.software, 'Sound Grinder Pro')
        self.assertEqual(info.created_date, '2010-12-28')
        self.assertEqual(info.engineer, 'JPH')
        self.assertEqual(info.keywords, 'Sound Effect, movement, microphone, bump')
        self.assertEqual(info.title, 'camera bumb 1')
        self.assertEqual(type(info.to_dict()), dict)
        self.assertEqual(type(info.__repr__()), str)

