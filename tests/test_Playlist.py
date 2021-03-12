from wavPlayer.Playlist import Playlist
from wavPlayer.Song import Song
import unittest


class TestPlaylist(unittest.TestCase):
    def setUp(self):
        self.song = Song("Summer hit 2020", "2020-03-14 16:26:36")
        self.playlist = Playlist("Summer hits",
                                 "2020-03-14 16:16:36",
                                 4,
                                 0.89,
                                 [self.song, Song("2", "2019"), Song("3", "2018")],
                                 None,
                                 "")

    def test_getTitle(self):
        self.assertEqual(self.playlist.getTitle(), "Summer hits")

    def test_getSongFromTitle(self):
        title = "Summer hit 2020"
        self.assertEqual(self.song, self.playlist.getSongFromTitle(title))
        title = "Wrong song for this playlist"
        self.assertRaises(KeyError, self.playlist.getSongFromTitle, title)

    def test_getData(self):
        correctOutput = {"Creation date": "2020-03-14 16:16:36",
                         "Number of times played": 4,
                         "Number of hours played": 0.89,
                         "First song": {},
                         "Changes history": ""}

        self.assertEqual(correctOutput, self.playlist.getData())

    def test_removeSong(self):
        self.playlist.removeSong(self.song)
        self.assertEqual("- Summer hit 2020\n", self.playlist.getChangesHistory())

    def test_changeOrder(self):
        self.assertEqual(["Summer hit 2020", "2", "3"], self.playlist.getSongsTitles())
        newOrder = ["3", "Summer hit 2020", "2"]
        self.playlist.changeOrder(newOrder)
        self.assertEqual(["3", "Summer hit 2020", "2"], self.playlist.getSongsTitles())


if __name__ == '__main__':
    unittest.main()
