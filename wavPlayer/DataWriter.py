from wavPlayer.Playlist import Playlist
from wavPlayer.Song import Song
from wavPlayer.constants import PLAYLISTS_DATA_PATH, COLLECTED_DATA_PATH, WAV_DIRECTORY_PATH
from datetime import datetime as date
from glob import glob
from pathlib import Path
import json


class DataWriter:
    """
    + saveData
    + changeNameOfPlaylist
    + removePlaylist
    + updatePlaylists
    + updateSongsData
    + generatePlaylistsAndSongs
    """
    def __init__(self, playlistPath=PLAYLISTS_DATA_PATH, collectedDataPath=COLLECTED_DATA_PATH):
        self.playlistPath = playlistPath
        self.collectedDataPath = collectedDataPath
        # Loads the playlistData json file and if it can't be found, it will be created
        try:
            with open(playlistPath) as playlistsDataFile:
                self.playlistsData = json.load(playlistsDataFile)
        except FileNotFoundError:
            with open(playlistPath, "w") as playlistsDataFile:
                json.dump({"All": []}, playlistsDataFile, indent=4)
            self.__init__()

        # Loads the collectedData json file and if it can't be found, it will be created
        try:
            with open(collectedDataPath) as collectedDataFile:
                self.collectedData = json.load(collectedDataFile)
        except FileNotFoundError:
            with open(collectedDataPath, "w") as collectedDataFile:
                json.dump({
                    "Playlists data": {
                        "All": {
                            "Creation date": str(date.today()),
                            "Number of times played": 0,
                            "Number of hours played": 0,
                            "First song": {},
                            "Changes history": ""
                        }
                    },
                    "Songs data": {}}, collectedDataFile, indent=4)
            self.__init__()

    def saveData(self):
        with open(self.playlistPath, "w") as playlistsDataFile:
            json.dump(self.playlistsData, playlistsDataFile, indent=4)

        with open(self.collectedDataPath, "w") as collectedDataFile:
            json.dump(self.collectedData, collectedDataFile, indent=4)

    def changeNameOfPlaylist(self, oldName: str, newName: str):
        if oldName not in self.playlistsData:
            raise ValueError("Playlist {} doesn't exist.".format(oldName))

        # Changes the playlist name in the collectedData json file, keeping its stats.
        data = self.collectedData["Playlists data"][oldName]
        self.collectedData["Playlists data"][newName] = data
        del self.collectedData["Playlists data"][oldName]

        # Changes the playlist name in the playlistData json file, keeping its list.
        data = self.playlistsData[oldName]
        self.playlistsData[newName] = data
        del self.playlistsData[oldName]

        self.saveData()

    def removePlaylist(self, playlistName: str):
        newName = "(DELETED) {}".format(playlistName)
        self.changeNameOfPlaylist(playlistName, newName)

        del self.playlistsData[newName]

        self.saveData()

    def updatePlaylists(self, playlistsDict: dict):
        # Updates and saves all changes made by the user to the playlists.
        for title in playlistsDict:
            playlist = playlistsDict[title]
            self.collectedData["Playlists data"][playlist.getTitle()] = playlist.getData()
            self.playlistsData[title] = playlist.getSongsTitles()
        self.saveData()

    def updateSongsData(self, songsDict: dict):
        # Updates and saves all new stats of the songs.
        for title in songsDict:
            song = songsDict[title]
            self.collectedData["Songs data"][title] = song.getData()
        self.saveData()

    def generatePlaylistsAndSongs(self) -> tuple:
        # Builds and returns the two dictionaries that will be used by the WAVPlayer class.
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
                # If a new .wav file has been added to the directory ./wavFiles, its stats will be initialized
                addedDate = str(date.today())
                timesPlayed = 0
                hoursPlayed = 0
                numberOfPlaylist = 0
                self.playlistsData["All"].append(title)

            songsDict[title] = Song(title, addedDate, timesPlayed, hoursPlayed, numberOfPlaylist)

        for title in self.playlistsData:
            songs = self.playlistsData[title]
            songsObjects = [songsDict[name] for name in songs]
            data = self.collectedData["Playlists data"][title]
            creationDate = data["Creation date"]
            timesPlayed = data["Number of times played"]
            hoursPlayed = data["Number of hours played"]
            firstSong = data["First song"]
            changesHistory = data["Changes history"]
            playlistsDict[title] = Playlist(title, creationDate, timesPlayed, hoursPlayed,
                                            songsObjects, firstSong, changesHistory)

        return playlistsDict, songsDict
