from pygame import mixer
from wavPlayer.constants import WAV_DIRECTORY_PATH


class MusicPlayer:
    """
    methods:
    + load
    + play
    + pause
    + unpause
    + stop
    + changeSong
    + isBusy
    + changeVolume
    + fadeAndExit
    + getLengthOfSong
    + getPercentagePlayed
    + getMinutesPlayed
    """
    def __init__(self):
        mixer.init()
        self.mixer = mixer.music
        self.sound = None

    def load(self, path):
        self.mixer.load(path)
        self.sound = mixer.Sound(path)

    def play(self):
        self.mixer.play()

    def pause(self):
        self.mixer.pause()

    def unpause(self):
        self.mixer.unpause()

    def stop(self):
        self.mixer.stop()

    def changeSong(self, newpath):
        self.load(newpath)
        self.play()

    def isBusy(self) -> bool:
        return self.mixer.get_busy()

    def changeVolume(self, volume):
        self.mixer.set_volume(volume)

    # TODO: check how to implement below method
    def fadeAndExit(self, time):
        pass
    #     self.mixer.fadeout(time)
    #     self.root.after(time, self.root.destroy)

    def getLengthOfSong(self) -> float:
        return self.sound.get_length()

    def getPercentagePlayed(self) -> float:
        try:
            return self.mixer.get_pos() / 1000 / self.getLengthOfSong()
        except AttributeError:
            return 0

    def getMinutesPlayed(self) -> float:
        length = self.getLengthOfSong()
        percentage = self.getPercentagePlayed()
        return length * percentage / 60


if __name__ == '__main__':
    from tkinter import *
    root = Tk()
    player = MusicPlayer()
    player.play()

    root.mainloop()
