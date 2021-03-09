from wavPlayer.Song import Song
import unittest


class TestSong(unittest.TestCase):

    def setUp(self):
        self.song = Song("Summer hit 2020", "2020-03-14 16:26:36")

    def test_getTitle(self):
        self.assertEqual(self.song.getTitle(), "Summer hit 2020")


if __name__ == '__main__':
    unittest.main()
