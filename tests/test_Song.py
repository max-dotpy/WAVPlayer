from wavPlayer.Song import Song
import unittest


class TestSong(unittest.TestCase):

    def setUp(self):
        self.song = Song("Summer hit 2020",
                         "2020-03-14 16:26:36",
                         4,
                         0.46,
                         1)

    def test_getTitle(self):
        self.assertEqual(self.song.getTitle(), "Summer hit 2020")

    def test_getData(self):
        correctOutput = {"Added date": "2020-03-14 16:26:36",
                         "Number of times played": 4,
                         "Number of hours played": 0.46,
                         "Number of playlists it is in": 1}

        self.assertEqual(self.song.getData(), correctOutput)

    def test_removedFromPlaylist(self):
        self.song.removedFromPlaylist()
        self.assertEqual(self.song.getNumberOfPlaylist(), 0)

        self.song.removedFromPlaylist()
        self.assertEqual(self.song.getNumberOfPlaylist(), 0)

    def test___eq__(self):
        copyOfSong = Song("Summer hit 2020", "2020-03-14 16:26:36", 4, 0.46, 1)
        self.assertEqual(copyOfSong, self.song)


if __name__ == '__main__':
    unittest.main()
