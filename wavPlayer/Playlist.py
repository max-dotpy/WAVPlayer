class Playlist:
    def __init__(self, title, creationDate, timesPlayed=0,
                 hoursPlayed=0, songs=None, firstSong=None, changesHistory=""):
        if title.startswith("(DELETED)"):
            raise KeyError
        self.title = title
        self.creationDate = creationDate
        self.timesPlayed = timesPlayed
        self.hoursPlayed = hoursPlayed
        self.songs = [] if songs is None else songs
        self.firstSongDict = {} if firstSong is None else firstSong
        self.changesHistory = changesHistory

    def getTitle(self) -> str:
        return self.title

    def getCreationDate(self) -> str:
        return self.creationDate

    def getTimesPlayed(self) -> int:
        return self.timesPlayed

    def getHoursPlayed(self) -> float:
        return self.hoursPlayed

    def getSongs(self) -> list:
        return self.songs

    def getSongsTitles(self) -> list:
        return [song.getTitle() for song in self.getSongs()]

    def getNumberOfSongs(self) -> int:
        return len(self.songs)

    def getFirstSongDict(self) -> dict:
        return self.firstSongDict

    def getChangesHistory(self) -> str:
        return self.changesHistory

    def played(self):
        self.timesPlayed += 1

    def playedFor(self, minutes):
        self.hoursPlayed += minutes / 60

    def firstSongPicked(self, song):
        if song in self.firstSongDict:
            self.firstSongDict[song] += 1
        else:
            self.firstSongDict[song] = 1

    def addChanges(self, sign, title):
        self.changesHistory += "{} {}\n".format(sign, title)

    def addSong(self, song):
        self.songs.append(song)
        self.addChanges("+", song.getTitle())

    def removeSong(self, song):
        del self.songs[self.songs.index(song)]
        self.addChanges("-", song.getTitle())

    def isDeleted(self) -> bool:
        return self.getTitle().startswith("(DELETED)")

    def getData(self) -> dict:
        return {"Creation date": self.getCreationDate(),
                "Number of times played": self.getTimesPlayed(),
                "Number of hours played": self.getHoursPlayed(),
                "First song": self.getFirstSongDict(),
                "Changes history": self.getChangesHistory()}

    def __str__(self) -> str:
        return self.getTitle()
