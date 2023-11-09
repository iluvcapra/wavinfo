from unittest import TestCase

import wavinfo
from wavinfo.wave_dbmd_reader import SegmentType, DolbyDigitalPlusMetadata

class TestDolby(TestCase):
    def setUp(self):
        self.test_file = "tests/test_files/protools/Test_ADM_ProTools.wav"

    def test_version(self):
        t1 = wavinfo.WavInfoReader(self.test_file)
        d = t1.dolby
        
        assert d is not None
        self.assertEqual((1,0,0,6), d.version)

    def test_segments(self):
        t1 = wavinfo.WavInfoReader(self.test_file)
        d = t1.dolby
        assert d is not None

        ddp = [x for x in d.segment_list \
                if x[0] == SegmentType.DolbyDigitalPlus]
        atmos = [x for x in d.segment_list \
                if x[0] == SegmentType.DolbyAtmos]

        self.assertEqual(len(ddp), 1)
        self.assertEqual(len(atmos), 1)

    def test_checksums(self):
        t1 = wavinfo.WavInfoReader(self.test_file)
        d = t1.dolby
        assert d is not None

        for seg in d.segment_list:
            self.assertTrue(seg[1])

    def test_ddp(self):
        t1 = wavinfo.WavInfoReader(self.test_file)
        d = t1.dolby
        assert d is not None
        ddp = d.dolby_digital_plus()
        self.assertEqual(len(ddp), 1, 
                         ("Failed to find exactly one Dolby Digital Plus " 
                          "metadata segment")
                         )

        self.assertTrue( ddp[0].audio_coding_mode, 
                        DolbyDigitalPlusMetadata.AudioCodingMode.CH_ORD_3_2 )
        self.assertTrue( ddp[0].lfe_on)
        
    def test_atmos(self):
        t1 = wavinfo.WavInfoReader(self.test_file)
        d = t1.dolby
        assert d is not None
        atmos = d.dolby_atmos()
        self.assertEqual(len(atmos), 1, 
                         "Failed to find exactly one Atmos metadata segment")

    
