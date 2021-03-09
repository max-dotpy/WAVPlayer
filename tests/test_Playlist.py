from wavPlayer.Playlist import Playlist
import unittest


class TestPlaylist(unittest.TestCase):

    def setUp(self):
        self.playlist = Playlist("Summer hits", "2020-03-14 16:16:36")

    def test_getTitle(self):
        self.assertEqual(self.playlist.getTitle(), "Summer hits")


if __name__ == '__main__':
    unittest.main()
