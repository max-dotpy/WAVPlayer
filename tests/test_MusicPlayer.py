from wavPlayer.MusicPlayer import MusicPlayer
from wavPlayer.constants import MOCKING_WAV_PATH
from tkinter import Tk
import unittest


class TestMusicPlayer(unittest.TestCase):
    def setUp(self):
        self.player = MusicPlayer()
        self.player.load(MOCKING_WAV_PATH)
        self.player.play()
        self.player.pause()
        self.root = Tk()
        self.root.geometry("0x0")

    def tearDown(self):
        self.root.after(10, lambda *args: self.root.destroy())
        self.root.mainloop()

    def test_isBusy(self):
        self.assertEqual(self.player.isBusy(), 1)

    def test_play(self):
        self.player.play()
        self.assertEqual(self.player.isBusy(), 1)

    def test_getLengthOfSong(self):
        self.assertEqual(33, int(self.player.getLengthOfSong()))


if __name__ == '__main__':
    unittest.main()

