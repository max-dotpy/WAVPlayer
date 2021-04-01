from wavPlayer.DataWriter import DataWriter
from wavPlayer.Playlist import Playlist
from wavPlayer.MusicPlayer import MusicPlayer
from wavPlayer.GUIComponents import GUI
from datetime import datetime as date


class WAVPlayer:
    """
        This class merges all the other classes together.
    """

    def __init__(self, root):
        # Initialize WAVPlayer instance variables that will be needed.
        self.root = root
        self.currentPlaylist = None
        self.currentSong = None
        self.currentOrder = []
        self.otherOrder = []
        self.currentIndex = -1
        self.firstTime = True
        self.newPlaylist = None

        # Initialize the Music Player.
        self.musicPlayer = MusicPlayer()

        # Initialize the DataWriter loading the playlists and songs dictionaries.
        self.dataWriter = DataWriter()
        self.playlistsDict, self.songsDict = self.loadData()

        # Start the GUI and load Playlists titles in the Listbox.
        self.gui = GUI(root)
        self.gui.table.fillPlaylistListbox(self.getSortedPlaylistsTitles())

        # Set all the root bindings.
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
        self.root.bind("<<BinPlaylist clicked>>", lambda *args: self.binClickedFirst())
        self.root.bind("<<BinSong clicked>>", lambda *args: self.binClickedFirst())
        self.root.bind("<<AddPlaylist clicked>>", lambda *args: self.addClickedWithPlaylistFirst())
        self.root.bind("<<AddSong clicked>>", lambda *args: self.addClickedWithSongFirst())
        self.root.bind("<<GearPlaylist clicked>>", lambda *args: self.gearClickedWithPlaylistFirst())
        self.root.bind("<<GearSong clicked>>", lambda *args: self.gearClickedWithSongFirst())

    def loadData(self):
        return self.dataWriter.generatePlaylistsAndSongs()

    def getSortedPlaylistsTitles(self) -> list:
        return sorted(list(self.playlistsDict.keys()))

    def playlistClicked(self):
        """
            This method is called when user clicks a Playlist.
        """

        table = self.gui.table
        # This is needed for resetting the currentIndex after the first playlist changes.
        if self.currentPlaylist is not None:
            self.currentIndex = -1
        index = table.playlistListbox.curselection()[0]
        title = self.getSortedPlaylistsTitles()[index]
        playlist = self.playlistsDict[title]
        songs = playlist.getSongsTitles()
        self.currentPlaylist = playlist
        table.fillSongListbox(songs)
        table.switchListbox()
        playlist.played()

    def songClicked(self):
        """
            This method is called when user clicks a Song.
        """

        table = self.gui.table
        index = table.songListbox.curselection()[0]
        song = self.currentPlaylist.getSongs()[index]
        # This gets into the stats that this song has been picked as first.
        self.currentPlaylist.firstSongPicked(song.getTitle())

        # This checks if the user wants a random shuffle of the playlist or not.
        randomState = self.gui.controls.buttonsFrame.randomButton.getState()
        randomOrder = self.currentPlaylist.getRandomizedPlaylist(song.getTitle())
        normalOrder = self.currentPlaylist.getOrderedPlaylist(song.getTitle())
        if randomState:
            self.currentOrder = randomOrder
            self.otherOrder = normalOrder
        else:
            self.currentOrder = normalOrder
            self.otherOrder = randomOrder

        self.playPlaylist()
        table.switchListbox()

    def playPlaylist(self):
        """
            This method is called when a song should start playing, it also begins the looper method.
        """

        self.nextSong()
        self.looper()

    def nextSong(self) -> bool:
        # If a song has been played, its stats will be updated.
        if self.currentSong is not None:
            self.currentSong.played()
            timePlayed = self.musicPlayer.getMinutesPlayed()
            self.currentSong.playedFor(timePlayed)
            self.currentPlaylist.playedFor(timePlayed)

        length = len(self.currentOrder)
        self.currentIndex += 1
        if self.currentIndex >= length:
            # If the user chose to repeat the playlist, it will cycle the same songs again, otherwise it stops.
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

        # This checks if the method has been called for the first time or not. It's needed to set properly
        # the Pause/Play Buttons.
        if self.firstTime:
            self.gui.controls.buttonsFrame.switchPausePlay()
            self.firstTime = False
        return True

    def looper(self):
        self.gui.controls.progressBar.progress(self.musicPlayer.getPercentagePlayed())
        if not self.musicPlayer.isBusy():
            if not self.nextSong():
                return
        self.root.after(1000, self.looper)

    def randomButtonClicked(self):
        """
            This method swaps between random shuffled Playlist, and normal Playlist, fixing the current index.
        """

        if self.currentOrder:
            newIndex = self.otherOrder.index(self.currentOrder[self.currentIndex])
            copy = self.currentOrder[:]
            self.currentOrder = self.otherOrder
            self.otherOrder = copy
            self.currentIndex = newIndex

    def search(self):
        """
            This method is called when the User presses Return/Enter.
        """

        if self.gui.table.currentListbox == "playlist":
            self.gui.table.searchListbox(self.getSortedPlaylistsTitles())
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
        # If the song has been played for more than 5 seconds, then it restarts. If not, the player changes
        # to previous song.
        if self.musicPlayer.getMinutesPlayed() * 60 >= 5:
            self.musicPlayer.stop()
        else:
            self.currentIndex -= 1
            if self.currentIndex < 0:
                self.currentIndex = len(self.currentOrder) - 1

            title = self.currentOrder[self.currentIndex]
            song = self.currentPlaylist.getSongFromTitle(title)
            self.gui.controls.setTitleOfSong(title)
            self.musicPlayer.load(song.getSongPath())
            song.played()
            minutes = self.musicPlayer.getLengthOfSong()
            song.playedFor(minutes / 60)
            self.currentPlaylist.playedFor(minutes / 60)

        self.musicPlayer.play()
        self.gui.controls.progressBar.restart()

    def fadeAndExit(self):
        self.musicPlayer.fadeAndExit(self.root)

    def binClickedFirst(self):
        """
            Method called when the Bin Button is clicked one time.
        """

        table = self.gui.table
        if table.currentListbox == "playlist":
            word = "playlist"
            table.setPlaylistListboxCommand(lambda *args: None)
            self.root.bind("<<BinPlaylist clicked>>", lambda *args: self.binClickedWithPlaylistSecond())
        else:
            word = "songs"
            table.setSongListboxCommand(lambda *args: None)
            table.songListbox.configure(selectmode="multiple")
            self.root.bind("<<BinSong clicked>>", lambda *args: self.binClickedWithSongSecond())

        self.gui.controls.setTitleOfSong(
            "<-- Click which {} you want to delete, then click the bin again".format(word))

    def binClickedWithPlaylistSecond(self):
        """
            Method called the second time the Bin Button is called and there was the Playlists Listbox.
        """

        index = self.gui.table.playlistListbox.curselection()[0]
        title = self.getSortedPlaylistsTitles()[index]
        for song in self.playlistsDict[title].getSongs():
            song.removedFromPlaylist()
        self.dataWriter.updatePlaylists(self.playlistsDict)
        self.dataWriter.updateSongsData(self.songsDict)

        self.gui.table.playlistListbox.delete(index)
        self.dataWriter.removePlaylist(title)
        self.playlistsDict, self.songsDict = self.loadData()

        self.gui.table.setPlaylistListboxCommand(lambda *args: self.gui.table.playlistClicked())
        self.gui.controls.setTitleOfSong("")
        self.root.bind("<<BinPlaylist clicked>>", lambda *args: self.binClickedFirst())

    def binClickedWithSongSecond(self):
        """
            Method called the second time the Bin Button is called and there was the Songs Listbox.
        """

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
        self.root.bind("<<BinSong clicked>>", lambda *args: self.binClickedFirst())

    def addClickedWithPlaylistFirst(self):
        """
            Method called when user clicks the + Button, first part of the process to create a new Playlist.
        """

        searchEntry = self.gui.table.searchEntry
        searchEntry.delete(0, "end")
        searchEntry.insert("end", "Playlist name?")
        searchEntry.selection_range(0, "end")
        searchEntry.focus()
        self.gui.controls.setTitleOfSong("<-- Choose what songs you want to add to the playlist, then click + again")

        # Unbind the Return key from the searchEntry.
        self.gui.table.setReturnEntryCommand(lambda *args: None)

        self.gui.table.showAllSongsListbox()
        self.gui.table.fillAllSongsListbox(sorted(list(self.songsDict.keys())))
        self.newPlaylist = Playlist("", str(date.today()))

        self.root.bind("<<AddPlaylist clicked>>", lambda *args: self.addClickedWithPlaylistSecond())

    def addClickedWithSongFirst(self):
        """
            Method called when user clicks the + Button, first part of the process to add Songs to a Playlist.
        """

        self.gui.controls.setTitleOfSong("<-- Click which songs you want to add, then click the + again")
        lst = list(self.songsDict.keys())
        for song in self.currentPlaylist.getSongsTitles():
            del lst[lst.index(song)]
        lst = sorted(lst)
        self.gui.table.fillAllSongsListbox(lst)

        self.gui.table.showAllSongsListbox()
        self.gui.table.update()

        self.root.bind("<<AddSong clicked>>", lambda *args: self.addClickedWithSongSecond())

    def addClickedWithPlaylistSecond(self):
        """
            Method called after the first part of the process to create a new Playlist.
        """

        table = self.gui.table
        indexes = table.allSongsListbox.curselection()
        table.hideAllSongsListbox()
        for index in indexes:
            name = sorted(list(self.songsDict.keys()))[index]
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
        table.fillPlaylistListbox(self.getSortedPlaylistsTitles())
        self.root.bind("<<AddPlaylist clicked>>", lambda *args: self.addClickedWithPlaylistFirst())

    def addClickedWithSongSecond(self):
        """
            Method called after the first part of the process to add new Songs to a Playlist.
        """

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
        """
            Method called when user clicks the Gear Button, first part of the process to change a Playlist's name.
        """

        self.gui.table.searchEntry.delete(0, "end")
        self.gui.table.searchEntry.insert("end", "Playlist new name?")
        self.gui.table.searchEntry.selection_range(0, "end")
        self.gui.table.searchEntry.focus()
        self.gui.controls.setTitleOfSong("<-- Choose a playlist and its new name, then click the gear again")
        self.gui.table.setReturnEntryCommand(lambda *args: None)
        self.gui.table.setPlaylistListboxCommand(lambda *args: None)

        self.root.bind("<<GearPlaylist clicked>>", lambda *args: self.gearClickedWithPlaylistSecond())

    def gearClickedWithSongFirst(self):
        """
            Method called when user clicks the Gear Button,
            first part of the process of changing order of a Playlist's songs.
        """

        self.gui.controls.setTitleOfSong("<-- Select 2 songs to swap them, then click the gear again")
        self.gui.table.songListbox.configure(selectmode="multiple")
        self.gui.table.setSongListboxCommand(lambda *args: self.gui.table.swapSongsOrder())
        self.root.bind("<<GearSong clicked>>", lambda *args: self.gearClickedWithSongSecond())

    def gearClickedWithPlaylistSecond(self):
        """
            Method called after the first part of the process to change a Playlist's name.
        """

        table = self.gui.table
        index = table.playlistListbox.curselection()[0]
        titleToChange = self.getSortedPlaylistsTitles()[index]
        newTitle = table.searchEntry.get()
        self.dataWriter.changeNameOfPlaylist(titleToChange, newTitle)
        self.playlistsDict, self.songsDict = self.loadData()
        table.searchEntry.delete(0, "end")
        table.setReturnEntryCommand(lambda *args: self.search())
        self.gui.controls.setTitleOfSong("")
        table.fillPlaylistListbox(self.getSortedPlaylistsTitles())
        table.setPlaylistListboxCommand(lambda *args: table.playlistClicked())
        self.root.bind("<<GearPlaylist clicked>>", lambda *args: self.gearClickedWithPlaylistFirst())

    def gearClickedWithSongSecond(self):
        """
            Method called after the first part of the process of changing order of a Playlist's songs.
        """

        newOrder = list(self.gui.table.songListbox.get(0, "end"))
        self.currentPlaylist.changeOrder(newOrder)
        self.gui.table.songListbox.configure(selectmode="browse")
        self.gui.controls.setTitleOfSong("")
        self.gui.table.setSongListboxCommand(lambda *args: self.gui.table.songClicked())
        self.root.bind("<<GearSong clicked>>", lambda *args: self.gearClickedWithSongFirst())
