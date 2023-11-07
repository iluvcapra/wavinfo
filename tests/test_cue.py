from unittest import TestCase
from glob import glob

import wavinfo

class TestCue(TestCase):
    def setUp(self) -> None:
        self.test_files = glob("tests/test_files/cue_chunks/*.wav") 
        return super().setUp()

    def test_enumerate(self):
        file1 = "tests/test_files/cue_chunks/STE-000.wav"
        w1 = wavinfo.WavInfoReader(file1)
        self.assertIsNotNone(w1.cues)
        vals = list(w1.cues.each_cue())
        self.assertEqual(vals, [(1,29616),(2,74592),(3,121200)])

    def test_labels_notes(self):
        file = "tests/test_files/cue_chunks/izotoperx_cues_test.wav"
        w1 = wavinfo.WavInfoReader(file)
        self.assertIsNotNone(w1.cues)
        assert w1.cues is not None

        for name, _ in w1.cues.each_cue():
            self.assertIn(name,[1,2,3])
            label, note = w1.cues.label_and_note(name)
            if name == 1:
                self.assertEqual("Marker 1", label)
                self.assertIsNone(note)

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

        assert w.cues is not None
        note = [n for n in w.cues.notes if n.name == 3]
        self.assertEqual(len(note), 1)
        self.assertEqual(note[0].text, expected)

    def test_label(self):
        file = "tests/test_files/cue_chunks/izotoperx_cues_test.wav"
        w = wavinfo.WavInfoReader(file)
        
        self.assertIsNotNone(w.cues)
        assert w.cues is not None  

        self.assertEqual(len(w.cues.labels), 3)
        for label in w.cues.labels:
            self.assertIn(label.name, [1,2,3])
            if label.name == 1:
                self.assertEqual(label.text, "Marker 1")
            elif label.name == 2:
                self.assertEqual(label.text, "Marker 2")
            elif label.name == 3:
                self.assertEqual(label.text, "Marker 3")




