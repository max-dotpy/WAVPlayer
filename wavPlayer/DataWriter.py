from wavPlayer.Playlist import Playlist
from wavPlayer.Song import Song
from wavPlayer.constants import PLAYLISTS_DATA_PATH, COLLECTED_DATA_PATH
from datetime import datetime as date
import json


class DataWriter:
    def __init__(self):
        with open(PLAYLISTS_DATA_PATH) as playlistsDataFile:
            self.playlistsData = json.load(playlistsDataFile)

        with open(COLLECTED_DATA_PATH) as collectedDataFile:
            self.collectedData = json.load(collectedDataFile)

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

    def updatePlaylists(self, playlists):
        for playlist in playlists:
            self.collectedData["Playlists data"][playlist] = playlist.getData()

        self.saveData()

    # TODO: implement this
    def addSong(self):
        pass
