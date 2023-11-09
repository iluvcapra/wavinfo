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

        assert adm is not None
        self.assertEqual(len(adm.channel_uids), 14)

    def test_to_dict(self):
        info = wavinfo.WavInfoReader(self.protools_adm_wav)
        adm = info.adm
        assert adm is not None
        dict = adm.to_dict()
        self.assertIsNotNone(dict)
    
    def test_programme(self):
        info = wavinfo.WavInfoReader(self.protools_adm_wav)
        adm = info.adm
        assert adm is not None
        pdict = adm.programme()
        self.assertIn("programme_id", pdict.keys())
        self.assertIn("programme_name", pdict.keys())
        self.assertEqual(pdict['programme_id'], 'APR_1001')
        self.assertEqual(pdict['programme_name'], 'Atmos_Master')
        self.assertIn("contents", pdict.keys())
        self.assertEqual(len(pdict["contents"]), 3)

    def test_track_info(self):
        info = wavinfo.WavInfoReader(self.protools_adm_wav)
        adm = info.adm
        assert adm is not None
        t1 = adm.track_info(0)
        self.assertTrue("channel_format_name" in t1.keys())
        self.assertEqual("RoomCentricLeft", t1["channel_format_name"])

        self.assertTrue("pack_format_name" in t1.keys())
        self.assertEqual("AtmosCustomPackFormat1", t1["pack_format_name"])

        t10 = adm.track_info(10)
        self.assertTrue("content_name" in t10.keys())
        self.assertEqual("Dialog", t10["content_name"])
        
