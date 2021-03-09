from wavPlayer.MusicPlayer import MusicPlayer
from tkinter import *
import unittest


class TestPlaylist(unittest.TestCase):

    def setUp(self):
        self.player = MusicPlayer()
        self.root = Tk()
        self.root.geometry("0x0")

    def test_play(self):
        self.player.play()
        self.assertEqual(self.player.isBusy(), 1)
        self.root.after(10, lambda *args: self.root.destroy())
        self.root.mainloop()


if __name__ == '__main__':
    unittest.main()
