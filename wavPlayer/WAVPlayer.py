from wavPlayer.constants import *
from wavPlayer.DataWriter import DataWriter
from wavPlayer.Playlist import Playlist
from wavPlayer.Song import Song
from wavPlayer.MusicPlayer import MusicPlayer
from wavPlayer.GUIComponents import GUI


class WAVPlayer:
    def __init__(self, root):
        self.root = root

        # Initialize the music player
        self.musicPlayer = MusicPlayer()

        # Initialize the DataWriter loading the playlists dict and songs dict,
        # it also create a Song class for all the new .wav files found
        self.dataWriter = DataWriter()
        self.playlistsDict, self.songsDict = self.dataWriter.generatePlaylistsAndSongs()

        # Start the GUI and load Playlists titles in the Listbox, and commands for +, gear, bin, search
        self.gui = GUI(root)
        self.gui.table.fillPlaylistListbox(sorted(list(self.playlistsDict.keys())))
        self.gui.table.setCurrentPlaylistsTitles(sorted(list(self.playlistsDict.keys())))
        self.gui.table.setPlaylistsDict(self.playlistsDict)
        self.gui.table.setMusicPlayer(self.musicPlayer)
        self.gui.table.setRandomButton(self.gui.controls.buttonsFrame.randomButton)
        self.gui.table.setRandomButton(self.gui.controls.buttonsFrame.reloadButton)


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.geometry("{}x{}+720+100".format(GUI_WIDTH, GUI_HEIGHT))
    root.title("")

    player = WAVPlayer(root)

    root.mainloop()
