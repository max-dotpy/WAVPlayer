from wavPlayer.constants import *
from wavPlayer.DataWriter import DataWriter
from wavPlayer.Playlist import Playlist
from wavPlayer.MusicPlayer import MusicPlayer
from wavPlayer.GUIComponents import GUI
from datetime import datetime as date
from tkinter import TclError


class WAVPlayer:
    def __init__(self, root):
        # Initialize WAVPlayer useful variables
        self.root = root
        self.currentPlaylist = None
        self.currentSong = None
        self.currentOrder = []
        self.otherOrder = []
        self.currentIndex = -1
        self.firstTime = True
        self.newPlaylist = None

        # Initialize the music player
        self.musicPlayer = MusicPlayer()

        # Initialize the DataWriter loading the playlists dict and songs dict,
        # it also create a Song class for all the new .wav files found
        self.dataWriter = DataWriter()
        self.playlistsDict, self.songsDict = self.dataWriter.generatePlaylistsAndSongs()

        # Start the GUI and load Playlists titles in the Listbox, and commands for +, gear, bin, search
        self.gui = GUI(root)
        self.gui.table.fillPlaylistListbox(sorted(list(self.playlistsDict.keys())))

        # Set all the root bindings
        self.gui.controls.buttonsFrame.setNextCommand(lambda *args: self.nextSong())
        self.gui.controls.buttonsFrame.setRandomCommand(lambda *args: self.randomButtonClicked())
        self.gui.table.setReturnEntryCommand(lambda *args: self.search())
        self.gui.table.setPlusButtonCommand(lambda *args: self.addPlaylistClickedFirstTime())
        self.gui.controls.buttonsFrame.setPauseCommand(lambda *args: self.pauseClicked())
        self.gui.controls.buttonsFrame.setPlayCommand(lambda *args: self.playClicked())
        self.gui.controls.buttonsFrame.setPrevCommand(lambda *args: self.prevClicked())
        self.root.bind("<<Playlist clicked>>", lambda *args: self.playlistClicked())
        self.root.bind("<<Song clicked>>", lambda *args: self.songClicked())
        self.root.bind("<<Volume changed>>", lambda *args: self.changeVolume())
        self.root.bind("<space>", lambda *args: self.pauseClicked())
        self.root.bind("<<Fade and exit>>", lambda *args: self.fadeAndExit())
        # TODO: IMPLEMENT THIS
        # self.root.bind("<<Statistics clicked>>", lambda *args: print("EHEHEHHE"))

    def playlistClicked(self):
        if self.currentPlaylist is None:
            table = self.gui.table
            index = table.playlistListbox.curselection()[0]
            title = sorted(list(self.playlistsDict.keys()))[index]
            songs = self.playlistsDict[title].getSongsTitles()
            self.currentPlaylist = self.playlistsDict[title]
            table.fillSongListbox(songs)
            table.switchListbox()
            self.playlistsDict[title].played()
        else:
            self.currentIndex = -1
            table = self.gui.table
            index = table.playlistListbox.curselection()[0]
            title = sorted(list(self.playlistsDict.keys()))[index]
            songs = self.playlistsDict[title].getSongsTitles()
            self.currentPlaylist = self.playlistsDict[title]
            table.fillSongListbox(songs)
            table.switchListbox()
            self.playlistsDict[title].played()

    def songClicked(self):
        table = self.gui.table
        index = table.songListbox.curselection()[0]
        song = self.currentPlaylist.getSongs()[index]
        self.currentPlaylist.firstSongPicked(song.getTitle())

        randomState = self.gui.controls.buttonsFrame.randomButton.getState()
        if randomState:
            self.currentOrder = self.currentPlaylist.getRandomizedPlaylist(song.getTitle())
            self.otherOrder = self.currentPlaylist.getOrderedPlaylist(song.getTitle())
        else:
            self.currentOrder = self.currentPlaylist.getOrderedPlaylist(song.getTitle())
            self.otherOrder = self.currentPlaylist.getRandomizedPlaylist(song.getTitle())

        self.playPlaylist()
        table.switchListbox()

    def playPlaylist(self):
        self.nextSong()
        self.gui.controls.progressBar.restart()
        self.looper()

    def nextSong(self) -> bool:
        if self.currentSong is not None:
            self.currentSong.played()
            timePlayed = self.musicPlayer.getMinutesPlayed()
            self.currentSong.playedFor(timePlayed)
            self.currentPlaylist.playedFor(timePlayed)

        length = len(self.currentOrder)
        self.currentIndex += 1
        if self.currentIndex >= length:
            if self.gui.controls.buttonsFrame.reloadButton.getState():
                self.currentIndex = 0
            else:
                self.gui.controls.buttonsFrame.switchPausePlay()
                self.musicPlayer.stop()
                self.gui.controls.setTitleOfSong("")
                self.gui.controls.progressBar.restart()
                return False
        title = self.currentOrder[self.currentIndex]
        song = self.currentPlaylist.getSongFromTitle(title)
        self.gui.controls.setTitleOfSong(title)
        self.musicPlayer.load(song.getSongPath())
        self.musicPlayer.play()
        song.played()
        minutes = self.musicPlayer.getLengthOfSong()
        song.playedFor(minutes / 60)
        self.currentPlaylist.playedFor(minutes / 60)
        self.gui.controls.progressBar.restart()

        if self.firstTime:
            self.gui.controls.buttonsFrame.switchPausePlay()
            self.firstTime = False
        return True

    def looper(self):
        self.gui.controls.progressBar.progress(self.musicPlayer.getPercentagePlayed())
        try:
            if not self.musicPlayer.isBusy():
                if not self.nextSong():
                    return

            self.root.after(1000, self.looper)
        except TclError:
            return None

    def randomButtonClicked(self):
        if self.currentOrder:
            newIndex = self.otherOrder.index(self.currentOrder[self.currentIndex])
            copy = self.currentOrder[:]
            self.currentOrder = self.otherOrder
            self.otherOrder = copy
            self.currentIndex = newIndex

    def search(self):
        if self.gui.table.currentListbox == "playlist":
            self.gui.table.searchListbox(sorted(list(self.playlistsDict.keys())))
        else:
            self.gui.table.searchListbox(self.currentPlaylist.getSongsTitles())

    def addPlaylistClickedFirstTime(self):
        self.gui.table.searchEntry.delete(0, "end")
        self.gui.table.searchEntry.insert("end", "Playlist name?")
        self.gui.table.searchEntry.selection_range(0, "end")
        self.gui.table.searchEntry.focus()
        self.gui.controls.setTitleOfSong("<-- Choose what songs you want to add to the playlist, then click + again")
        self.gui.table.setReturnEntryCommand(lambda *args: None)
        self.gui.table.showAllSongsListbox()
        self.gui.table.fillAllSongsListbox(sorted(list(self.songsDict.keys())))
        self.newPlaylist = Playlist("", str(date.today()))

        self.gui.table.setPlusButtonCommand(lambda *args: self.addPlaylistClickedSecondTime())

    def addPlaylistClickedSecondTime(self):
        table = self.gui.table
        indexes = table.allSongsListbox.curselection()
        self.gui.table.hideAllSongsListbox()
        for index in indexes:
            name = sorted(list(self.songsDict))[index]
            song = self.songsDict[name]
            self.newPlaylist.addSong(song)
        self.newPlaylist.setTitle(table.searchEntry.get())
        self.playlistsDict[table.searchEntry.get()] = self.newPlaylist

        table.searchEntry.delete(0, "end")
        table.setReturnEntryCommand(lambda *args: self.search())
        table.setPlusButtonCommand(lambda *args: self.addPlaylistClickedFirstTime())
        self.gui.controls.setTitleOfSong("")
        self.newPlaylist = None
        self.dataWriter.updatePlaylists(self.playlistsDict)
        self.dataWriter.updateSongsData(self.songsDict)
        self.gui.table.fillPlaylistListbox(sorted(list(self.playlistsDict.keys())))

    def changeVolume(self):
        percentage = self.gui.controls.volumeFrame.volumeBar.getVolumePercentage()
        self.musicPlayer.changeVolume(percentage)

    def pauseClicked(self):
        self.gui.controls.buttonsFrame.switchPausePlay()
        self.root.bind("<space>", lambda *args: self.playClicked())
        self.musicPlayer.pause()

    def playClicked(self):
        self.gui.controls.buttonsFrame.switchPausePlay()
        self.root.bind("<space>", lambda *args: self.pauseClicked())
        self.musicPlayer.unpause()

    def prevClicked(self):
        if self.musicPlayer.getMinutesPlayed() * 60 >= 5:
            self.musicPlayer.stop()
            self.musicPlayer.play()
            self.gui.controls.progressBar.restart()
        else:
            length = len(self.currentOrder)
            self.currentIndex -= 1
            if self.currentIndex < 0:
                self.currentIndex = length - 1

            title = self.currentOrder[self.currentIndex]
            song = self.currentPlaylist.getSongFromTitle(title)
            self.gui.controls.setTitleOfSong(title)
            self.musicPlayer.load(song.getSongPath())
            self.musicPlayer.play()
            song.played()
            minutes = self.musicPlayer.getLengthOfSong()
            song.playedFor(minutes / 60)
            self.currentPlaylist.playedFor(minutes / 60)
            self.gui.controls.progressBar.restart()

    def fadeAndExit(self):
        time = int(self.musicPlayer.getLengthOfSong() * (1 - self.musicPlayer.getPercentagePlayed())) * 1000
        self.musicPlayer.mixer.fadeout(time)
        self.root.after(time, self.root.destroy)


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.geometry("{}x{}+720+100".format(GUI_WIDTH, GUI_HEIGHT))
    root.title("")

    player = WAVPlayer(root)

    root.mainloop()

    player.dataWriter.updatePlaylists(player.playlistsDict)
    player.dataWriter.updateSongsData(player.songsDict)
