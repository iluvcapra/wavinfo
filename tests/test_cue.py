from unittest import TestCase
from glob import glob

import wavinfo

class TestCue(TestCase):
    def setUp(self) -> None:
        self.test_files = glob("tests/test_files/cue_chunks/*.wav") 
        return super().setUp()

    def test_encoding_fallback(self):
        """
        Added this after I noticed that iZotope RX seems to just encode "notes"
        as utf-8 without bothering to dump this info into the ltxt or 
        specifying an encoding by some other means.
        """
        file = "tests/test_files/cue_chunks/izotoperx_cues_test.wav"
        w = wavinfo.WavInfoReader(file, info_encoding='utf-8')
        expected = ("Лорем ипсум долор сит амет, тимеам вивендум хас ет, "  
            "цу адолесценс дефинитионес еам.")

        note = [n for n in w.cues.notes if n.name == 3]
        self.assertEqual(len(note), 1)
        self.assertEqual(note[0].text, expected)

    def test_label(self):
        file = "tests/test_files/cue_chunks/izotoperx_cues_test.wav"
        w = wavinfo.WavInfoReader(file)
        
        self.assertIsNotNone(w.cues)
        
        self.assertEqual(len(w.cues.labels), 3)
        for label in w.cues.labels:
            if label.name == 1:
                self.assertEqual(label.text, "Marker 1")
            elif label.name == 2:
                self.assertEqual(label.text, "Marker 2")
            elif label.name == 3:
                self.assertEqual(label.text, "Marker 3")
            else:
                self.fail(f"Encountered unexpected label id {label.name}")



