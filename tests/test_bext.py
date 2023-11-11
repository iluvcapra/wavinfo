import unittest

from wavinfo.scopes import wave_bext_reader


class TextBext(unittest.TestCase):
    def setUp(self):
        pass

    def test_roundtrip(self):
        bext = wave_bext_reader.Bext(version=2,
                                     description="Text text description",
                                     originator="wavinfo",
                                     originator_ref=
                                     "123456789012345678901234567890",
                                     originator_date="2023-11-10",
                                     originator_time="09:01:13",
                                     time_reference=10000999,
                                     coding_history="test_do_not_use;",
                                     umid=b"0XXXXXXXXX1XXXXXXXXX2XXXXXXXXX3XX",
                                     loudness_value=-24.3, loudness_range=8.1,
                                     max_true_peak=-2.2,
                                     max_momentary_loudness=-4.0,
                                     max_shortterm_loudness=-7.5)

        w, r = (wave_bext_reader.WavBextWriter(), 
                wave_bext_reader.WavBextReader(encoding='ascii'))
        
        bext_data = w.write(bext)
        received = r.read(bext_data)
        
        self.assertEqual(bext.description, received.description)
        self.assertEqual(bext.originator, received.originator)
        self.assertEqual(bext.originator_ref, received.originator_ref)
        self.assertEqual(bext.originator_date, received.originator_date)
        self.assertEqual(bext.originator_time, received.originator_time)
        self.assertEqual(bext.time_reference, received.time_reference)
        self.assertEqual(bext.version, received.version)
        self.assertEqual(bext.coding_history, received.coding_history)
        self.assertEqual(bext.umid[0:32], received.umid[0:32])
        self.assertAlmostEqual(bext.loudness_value, received.loudness_value)
        self.assertAlmostEqual(bext.loudness_range, received.loudness_range)
        self.assertAlmostEqual(bext.max_true_peak, received.max_true_peak)
        self.assertAlmostEqual(bext.max_momentary_loudness, 
                               received.max_momentary_loudness)
        self.assertAlmostEqual(bext.max_shortterm_loudness, 
                               received.max_shortterm_loudness)
