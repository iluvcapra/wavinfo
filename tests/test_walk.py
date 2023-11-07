import unittest
import wavinfo

import glob

class TestWalk(unittest.TestCase):
    def test_walk_metadata(self):
        test_file = 'tests/test_files/protools/PT A101_4.A1.wav'
        info = wavinfo.WavInfoReader(test_file)

        tested_data , tested_format = False, False
        for scope, key, value in info.walk():
            if scope == 'fmt':
                if key == 'channel_count':
                    tested_format = True
                    self.assertEqual(value, 2)
            if scope == 'data':
                if key == 'frame_count':
                    tested_data = True
                    self.assertEqual(value, 144140)

        self.assertTrue(tested_data and tested_format)

    def test_walk_all(self):
        for file in glob.glob('tests/test_files/**/*.wav'):
            info = wavinfo.WavInfoReader(file)
            
            try:
                for _, _, _ in info.walk():
                    pass 
            except:
                self.fail(f"Failed to walk metadata in file {file}")

        

if __name__ == '__main__':
    unittest.main()
