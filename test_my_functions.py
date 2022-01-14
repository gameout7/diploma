import unittest
import my_functions

class TestMyFUnctions(unittest.TestCase):
    """Tests for my functions"""

    def test_get_artist_id(self):
        band = 'beatles'
        artist_id = my_functions.get_artist_id(band)

        self.assertEqual(artist_id, 136975)

if __name__ == '__main__':
    unittest.main()