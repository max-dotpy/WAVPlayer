from wavPlayer.MusicPlayer import MusicPlayer
import unittest


class TestPlaylist(unittest.TestCase):

    def setUp(self):
        self.player = MusicPlayer()


if __name__ == '__main__':
    unittest.main()
