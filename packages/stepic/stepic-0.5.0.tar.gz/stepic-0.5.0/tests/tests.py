import unittest
import os
try:
    import stepic
except ImportError:
    import sys
    sys.path.append('../stepic')
    import stepic

class TestStepic(unittest.TestCase):

    def test_stepic(self):

        keep = False

        stepic.encode_files('tests/test_img.png', 'tests/test_text.txt', 'tests/encoded.png', None)
        stepic.decode_files('tests/encoded.png', 'tests/encoded.txt')
        textfile = open('tests/encoded.txt')
        text = textfile.read()
        textfile.close()
        if not keep:
            os.remove('tests/encoded.txt')
            os.remove('tests/encoded.png')
        self.assertEqual(text, "The quick brown fox jumped over the lazy dog.\n", "Decoded text incorrect")

if __name__ == '__main__':
    unittest.main()

