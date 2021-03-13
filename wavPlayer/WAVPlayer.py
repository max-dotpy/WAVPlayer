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
        self.playlistsDict, self.songsDict = self.loadData()

        # Start the GUI and load Playlists titles in the Listbox, and commands for +, gear, bin, search
        self.gui = GUI(root)
        self.gui.table.fillPlaylistListbox(sorted(list(self.playlistsDict.keys())))

        # Set all the root bindings
        self.gui.controls.buttonsFrame.setNextCommand(lambda *args: self.nextSong())
        self.gui.controls.buttonsFrame.setRandomCommand(lambda *args: self.randomButtonClicked())
        self.gui.table.setReturnEntryCommand(lambda *args: self.search())
        self.gui.controls.buttonsFrame.setPauseCommand(lambda *args: self.pauseClicked())
        self.gui.controls.buttonsFrame.setPlayCommand(lambda *args: self.playClicked())
        self.gui.controls.buttonsFrame.setPrevCommand(lambda *args: self.prevClicked())
        self.root.bind("<<Playlist clicked>>", lambda *args: self.playlistClicked())
        self.root.bind("<<Song clicked>>", lambda *args: self.songClicked())
        self.root.bind("<<Volume changed>>", lambda *args: self.changeVolume())
        self.root.bind("<space>", lambda *args: self.pauseClicked())
        self.root.bind("<<Fade and exit>>", lambda *args: self.fadeAndExit())
        self.root.bind("<<BinPlaylist clicked>>", lambda *args: self.binClickedWithPlaylistFirst())
        self.root.bind("<<BinSong clicked>>", lambda *args: self.binClickedWithSongFirst())
        self.root.bind("<<AddPlaylist clicked>>", lambda *args: self.addClickedWithPlaylistFirst())
        self.root.bind("<<AddSong clicked>>", lambda *args: self.addClickedWithSongFirst())
        self.root.bind("<<GearPlaylist clicked>>", lambda *args: self.gearClickedWithPlaylistFirst())
        self.root.bind("<<GearSong clicked>>", lambda *args: self.gearClickedWithSongFirst())
        # TODO: IMPLEMENT THIS
        # self.root.bind("<<Statistics clicked>>", lambda *args: print("EHEHEHHE"))

    def loadData(self):
        return self.dataWriter.generatePlaylistsAndSongs()

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
        self.musicPlayer.fadeAndExit(self.root)

    def binClickedWithPlaylistFirst(self):
        self.gui.controls.setTitleOfSong("<-- Click which playlist you want to delete, then click the bin again")
        self.gui.table.setPlaylistListboxCommand(lambda *args: None)
        self.root.bind("<<BinPlaylist clicked>>", lambda *args: self.binClickedWithPlaylistSecond())

    def binClickedWithPlaylistSecond(self):
        index = self.gui.table.playlistListbox.curselection()[0]
        title = sorted(list(self.playlistsDict.keys()))[index]
        for song in self.playlistsDict[title].getSongs():
            song.removedFromPlaylist()
        self.dataWriter.updatePlaylists(self.playlistsDict)
        self.dataWriter.updateSongsData(self.songsDict)

        self.gui.table.playlistListbox.delete(index)
        self.dataWriter.removePlaylist(title)
        self.playlistsDict, self.songsDict = self.loadData()

        self.gui.table.setPlaylistListboxCommand(lambda *args: self.gui.table.playlistClicked())
        self.gui.controls.setTitleOfSong("")
        self.root.bind("<<BinPlaylist clicked>>", lambda *args: self.binClickedWithPlaylistFirst())

    def binClickedWithSongFirst(self):
        self.gui.controls.setTitleOfSong("<-- Click which songs you want to delete, then click the bin again")
        self.gui.table.setSongListboxCommand(lambda *args: None)
        self.gui.table.songListbox.configure(selectmode="multiple")
        self.root.bind("<<BinSong clicked>>", lambda *args: self.binClickedWithSongSecond())

    def binClickedWithSongSecond(self):
        self.dataWriter.updatePlaylists(self.playlistsDict)
        self.dataWriter.updateSongsData(self.songsDict)

        indexes = self.gui.table.songListbox.curselection()
        playlist = self.currentPlaylist
        songs = []
        for index in indexes:
            songs.append(self.songsDict[playlist.getSongsTitles()[index]])
        for song in songs:
            playlist.removeSong(song)

        countDeleted = 0
        for index in indexes:
            self.gui.table.songListbox.delete(index - countDeleted)
            countDeleted += 1

        self.dataWriter.updatePlaylists(self.playlistsDict)
        self.dataWriter.updateSongsData(self.songsDict)

        self.playlistsDict, self.songsDict = self.loadData()

        self.gui.table.songListbox.configure(selectmode="browse")
        self.gui.table.setSongListboxCommand(lambda *args: self.gui.table.songClicked())
        self.gui.controls.setTitleOfSong("")
        self.root.bind("<<BinSong clicked>>", lambda *args: self.binClickedWithSongFirst())

    def addClickedWithPlaylistFirst(self):
        self.gui.table.searchEntry.delete(0, "end")
        self.gui.table.searchEntry.insert("end", "Playlist name?")
        self.gui.table.searchEntry.selection_range(0, "end")
        self.gui.table.searchEntry.focus()
        self.gui.controls.setTitleOfSong("<-- Choose what songs you want to add to the playlist, then click + again")
        self.gui.table.setReturnEntryCommand(lambda *args: None)
        self.gui.table.showAllSongsListbox()
        self.gui.table.fillAllSongsListbox(sorted(list(self.songsDict.keys())))
        self.newPlaylist = Playlist("", str(date.today()))

        self.root.bind("<<AddPlaylist clicked>>", lambda *args: self.addClickedWithPlaylistSecond())

    def addClickedWithPlaylistSecond(self):
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
        self.gui.controls.setTitleOfSong("")
        self.newPlaylist = None
        self.dataWriter.updatePlaylists(self.playlistsDict)
        self.dataWriter.updateSongsData(self.songsDict)
        self.gui.table.fillPlaylistListbox(sorted(list(self.playlistsDict.keys())))
        self.root.bind("<<AddPlaylist clicked>>", lambda *args: self.addClickedWithPlaylistFirst())

    def addClickedWithSongFirst(self):
        self.gui.controls.setTitleOfSong("<-- Click which songs you want to add, then click the + again")
        lst = list(self.songsDict.keys())
        for song in self.currentPlaylist.getSongsTitles():
            del lst[lst.index(song)]
        lst = sorted(lst)
        self.gui.table.fillAllSongsListbox(lst)

        self.gui.table.showAllSongsListbox()
        self.gui.table.update()

        self.root.bind("<<AddSong clicked>>", lambda *args: self.addClickedWithSongSecond())

    def addClickedWithSongSecond(self):
        self.dataWriter.updatePlaylists(self.playlistsDict)
        self.dataWriter.updateSongsData(self.songsDict)

        indexes = self.gui.table.allSongsListbox.curselection()
        lst = list(self.songsDict.keys())
        for song in self.currentPlaylist.getSongsTitles():
            del lst[lst.index(song)]
        lst = sorted(lst)
        songs = []
        for index in indexes:
            songs.append(self.songsDict[lst[index]])
        for song in songs:
            self.currentPlaylist.addSong(song)

        self.dataWriter.updatePlaylists(self.playlistsDict)
        self.dataWriter.updateSongsData(self.songsDict)

        self.playlistsDict, self.songsDict = self.loadData()

        songs = self.currentPlaylist.getSongsTitles()
        self.gui.table.fillSongListbox(songs)

        self.gui.table.hideAllSongsListbox()
        self.gui.controls.setTitleOfSong("")
        self.root.bind("<<AddSong clicked>>", lambda *args: self.addClickedWithSongFirst())

    def gearClickedWithPlaylistFirst(self):
        self.gui.table.searchEntry.delete(0, "end")
        self.gui.table.searchEntry.insert("end", "Playlist new name?")
        self.gui.table.searchEntry.selection_range(0, "end")
        self.gui.table.searchEntry.focus()
        self.gui.controls.setTitleOfSong("<-- Choose a playlist and its new name, then click the gear again")
        self.gui.table.setReturnEntryCommand(lambda *args: None)
        self.gui.table.setPlaylistListboxCommand(lambda *args: None)

        self.root.bind("<<GearPlaylist clicked>>", lambda *args: self.gearClickedWithPlaylistSecond())

    def gearClickedWithPlaylistSecond(self):
        table = self.gui.table
        index = table.playlistListbox.curselection()[0]
        titleToChange = sorted(list(self.playlistsDict.keys()))[index]
        newTitle = table.searchEntry.get()
        self.dataWriter.changeNameOfPlaylist(titleToChange, newTitle)
        self.playlistsDict, self.songsDict = self.loadData()
        table.searchEntry.delete(0, "end")
        table.setReturnEntryCommand(lambda *args: self.search())
        self.gui.controls.setTitleOfSong("")
        table.fillPlaylistListbox(sorted(list(self.playlistsDict.keys())))
        table.setPlaylistListboxCommand(lambda *args: table.playlistClicked())
        self.root.bind("<<GearPlaylist clicked>>", lambda *args: self.gearClickedWithPlaylistFirst())

    def gearClickedWithSongFirst(self):
        self.gui.controls.setTitleOfSong("<-- Select 2 songs to swap them, then click the gear again")
        self.gui.table.songListbox.configure(selectmode="multiple")
        self.gui.table.setSongListboxCommand(lambda *args: self.gui.table.swapSongsOrder())
        self.root.bind("<<GearSong clicked>>", lambda *args: self.gearClickedWithSongSecond())

    def gearClickedWithSongSecond(self):
        newOrder = list(self.gui.table.songListbox.get(0, "end"))
        self.currentPlaylist.changeOrder(newOrder)
        self.gui.table.songListbox.configure(selectmode="browse")
        self.gui.controls.setTitleOfSong("")
        self.gui.table.setSongListboxCommand(lambda *args: self.gui.table.songClicked())
        self.root.bind("<<GearSong clicked>>", lambda *args: self.gearClickedWithSongFirst())


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.geometry("{}x{}+720+100".format(GUI_WIDTH, GUI_HEIGHT))  # TODO: rendi fisso
    root.title("")

    player = WAVPlayer(root)

    root.mainloop()

    player.dataWriter.updatePlaylists(player.playlistsDict)
    player.dataWriter.updateSongsData(player.songsDict)
