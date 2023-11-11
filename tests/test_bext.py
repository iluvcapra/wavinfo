import unittest

from wavinfo.scopes import bext


class TextBext(unittest.TestCase):
    def setUp(self):
        pass

    def test_roundtrip(self):
        bext_struct = bext.Bext(version=2,
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


        bext_data = bext.write(bext_struct, encoding='ascii')
        received = bext.read(bext_data, encoding='ascii')
        
        self.assertEqual(bext_struct.description, received.description)
        self.assertEqual(bext_struct.originator, received.originator)
        self.assertEqual(bext_struct.originator_ref, received.originator_ref)
        self.assertEqual(bext_struct.originator_date, received.originator_date)
        self.assertEqual(bext_struct.originator_time, received.originator_time)
        self.assertEqual(bext_struct.time_reference, received.time_reference)
        self.assertEqual(bext_struct.version, received.version)
        self.assertEqual(bext_struct.coding_history, received.coding_history)
        self.assertEqual(bext_struct.umid[0:32], received.umid[0:32])
        self.assertAlmostEqual(bext_struct.loudness_value, received.loudness_value)
        self.assertAlmostEqual(bext_struct.loudness_range, received.loudness_range)
        self.assertAlmostEqual(bext_struct.max_true_peak, received.max_true_peak)
        self.assertAlmostEqual(bext_struct.max_momentary_loudness, 
                               received.max_momentary_loudness)
        self.assertAlmostEqual(bext_struct.max_shortterm_loudness, 
                               received.max_shortterm_loudness)
