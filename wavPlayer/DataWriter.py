from wavPlayer.Playlist import Playlist
from wavPlayer.Song import Song
from wavPlayer.constants import PLAYLISTS_DATA_PATH, COLLECTED_DATA_PATH, WAV_DIRECTORY_PATH
from datetime import datetime as date
from glob import glob
from pathlib import Path
import json


class DataWriter:
    """
    methods:
    + saveData
    + addNewPlaylist
    + removePlaylist
    + updatePlaylists
    + updateSongsData
    + generatePlaylistsAndSongs
    """
    def __init__(self):
        try:
            with open(PLAYLISTS_DATA_PATH) as playlistsDataFile:
                self.playlistsData = json.load(playlistsDataFile)
        except FileNotFoundError:
            with open(PLAYLISTS_DATA_PATH, "w") as playlistsDataFile:
                json.dump({"All": []}, playlistsDataFile, indent=4)
            self.__init__()

        try:
            with open(COLLECTED_DATA_PATH) as collectedDataFile:
                self.collectedData = json.load(collectedDataFile)
        except FileNotFoundError:
            with open(COLLECTED_DATA_PATH, "w") as collectedDataFile:
                json.dump({"Playlists data": {"All": {
                                              "Creation date": str(date.today()),
                                              "Number of times played": 0,
                                              "Number of hours played": 0,
                                              "First song": {},
                                              "Changes history": ""
                                              }
                                              }, "Songs data": {}}, collectedDataFile, indent=4)
            self.__init__()

    def saveData(self):
        with open(PLAYLISTS_DATA_PATH, "w") as playlistsDataFile:
            json.dump(self.playlistsData, playlistsDataFile, indent=4)

        with open(COLLECTED_DATA_PATH, "w") as collectedDataFile:
            json.dump(self.collectedData, collectedDataFile, indent=4)

    def addNewPlaylist(self, playlist):
        if playlist.getTitle() in self.playlistsData:
            raise KeyError
        titles = playlist.getSongsTitles()
        self.playlistsData[playlist.getTitle()] = titles

        firstChangesHistory = ""
        for title in titles:
            firstChangesHistory += "+ {}\n".format(title)

        self.collectedData["Playlists data"][playlist.getTitle()] = {
            "Creation date": str(date.today()),
            "Number of times played": 0,
            "Number of hours played": 0,
            "First song": {"Random": 0},
            "Changes history": firstChangesHistory
            }

        self.saveData()

    def removePlaylist(self, playlistName):
        if playlistName not in self.playlistsData:
            raise KeyError
        del self.playlistsData[playlistName]
        copyData = self.collectedData["Playlists data"][playlistName]
        del self.collectedData["Playlists data"][playlistName]
        self.collectedData["Playlists data"]["(DELETED) {}".format(playlistName)] = copyData

        self.saveData()

    def updatePlaylists(self, playlistsDict):
        for title in playlistsDict:
            playlist = playlistsDict[title]
            self.collectedData["Playlists data"][playlist.getTitle()] = playlist.getData()
            self.playlistsData[title] = playlist.getSongsTitles()
        self.saveData()

    def updateSongsData(self, songsDict):
        for title in songsDict:
            song = songsDict[title]
            self.collectedData["Songs data"][title] = song.getData()
        self.saveData()

    def generatePlaylistsAndSongs(self) -> tuple:
        playlistsDict = {}
        songsDict = {}
        for path in glob("{}/*.wav".format(WAV_DIRECTORY_PATH)):
            title = Path(path).stem
            if title in self.collectedData["Songs data"]:
                data = self.collectedData["Songs data"][title]
                addedDate = data["Added date"]
                timesPlayed = data["Number of times played"]
                hoursPlayed = data["Number of hours played"]
                numberOfPlaylist = data["Number of playlists it is in"]
            else:
                addedDate = str(date.today())
                timesPlayed = 0
                hoursPlayed = 0
                numberOfPlaylist = 0
                self.playlistsData["All"].append(title)

            songsDict[title] = Song(title, addedDate, timesPlayed, hoursPlayed, numberOfPlaylist)

        for title in self.playlistsData:
            songs = self.playlistsData[title]
            songsClasses = [songsDict[name] for name in songs]
            data = self.collectedData["Playlists data"][title]
            creationDate = data["Creation date"]
            timesPlayed = data["Number of times played"]
            hoursPlayed = data["Number of hours played"]
            firstSong = data["First song"]
            changesHistory = data["Changes history"]
            playlistsDict[title] = Playlist(title, creationDate, timesPlayed, hoursPlayed,
                                            songsClasses, firstSong, changesHistory)

        return playlistsDict, songsDict

    def changeNameOfPlaylist(self, oldName, newName):
        data = self.collectedData["Playlists data"][oldName]
        self.collectedData["Playlists data"][newName] = data
        del self.collectedData["Playlists data"][oldName]

        data = self.playlistsData[oldName]
        self.playlistsData[newName] = data
        del self.playlistsData[oldName]

        self.saveData()