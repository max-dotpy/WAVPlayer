from wavPlayer.WAVPlayer import WAVPlayer
from tkinter import Tk
from wavPlayer.constants import GUI_HEIGHT, GUI_WIDTH


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("{}x{}+720+100".format(GUI_WIDTH, GUI_HEIGHT))
        self.root.minsize(GUI_WIDTH, GUI_HEIGHT)
        self.root.maxsize(GUI_WIDTH, GUI_HEIGHT)
        self.root.title("")
        self.wavPlayer = None

    def run(self):
        self.wavPlayer = WAVPlayer(self.root)
        self.root.mainloop()
        self.save()

    def save(self):
        self.wavPlayer.dataWriter.updatePlaylists(self.wavPlayer.playlistsDict)
        self.wavPlayer.dataWriter.updateSongsData(self.wavPlayer.songsDict)


if __name__ == '__main__':
    Application().run()
