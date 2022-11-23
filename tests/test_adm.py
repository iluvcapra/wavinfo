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

    def test_to_dict(self):
        info = wavinfo.WavInfoReader(self.protools_adm_wav)
        adm = info.adm
        dict = adm.to_dict()
        self.assertIsNotNone(dict)
    
    def test_track_info(self):
        info = wavinfo.WavInfoReader(self.protools_adm_wav)
        adm = info.adm

        t1 = adm.track_info(0)
        self.assertTrue("channel_format_name" in t1.keys())
        self.assertEqual("RoomCentricLeft", t1["channel_format_name"])

        self.assertTrue("pack_format_name" in t1.keys())
        self.assertEqual("AtmosCustomPackFormat1", t1["pack_format_name"])

        t10 = adm.track_info(10)
        self.assertTrue("content_name" in t10.keys())
        self.assertEqual("Dialog", t10["content_name"])
        
