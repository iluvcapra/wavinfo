from unittest import TestCase

import wavinfo

class TestADMWave(TestCase):

    def setUp(self) -> None:
        self.protools_adm_wav = "tests/test_files/protools/Test_ADM_ProTools.wav"
        return super().setUp()

    def test_chna(self):
        info = wavinfo.WavInfoReader(self.protools_adm_wav)
        self.assertIsNotNone(info)

        adm = info.adm
        self.assertIsNotNone(adm)

        self.assertEqual(len(adm.channel_uids), 14)

    # def test_to_dict(self):
    #     info = wavinfo.WavInfoReader(self.protools_adm_wav)
    #     adm = info.adm
    #     dict = adm.to_dict()
        
