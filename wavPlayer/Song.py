from wavPlayer.constants import WAV_DIRECTORY_PATH


class Song:
    """
        It stores every information we need to work with Songs.
    """

    def __init__(self, title: str, addedDate: str, timesPlayed=0, hoursPlayed=0, numberOfPlaylist=0):
        self.title = title
        self.addedDate = addedDate
        self.timesPlayed = timesPlayed
        self.hoursPlayed = hoursPlayed
        self.numberOfPlaylist = numberOfPlaylist

    def getTitle(self) -> str:
        return self.title

    def getAddedDate(self) -> str:
        return self.addedDate

    def getTimesPlayed(self) -> int:
        return self.timesPlayed

    def getHoursPlayed(self) -> float:
        return self.hoursPlayed

    def getNumberOfPlaylist(self) -> int:
        return self.numberOfPlaylist

    def getSongPath(self) -> str:
        return "{}/{}.wav".format(WAV_DIRECTORY_PATH, self.getTitle())

    def getData(self) -> dict:
        return {"Added date": self.getAddedDate(),
                "Number of times played": self.getTimesPlayed(),
                "Number of hours played": self.getHoursPlayed(),
                "Number of playlists it is in": self.getNumberOfPlaylist()}

    def played(self):
        self.timesPlayed += 1

    def playedFor(self, minutes: float):
        self.hoursPlayed += minutes / 60

    def addedToPlaylist(self):
        self.numberOfPlaylist += 1

    def removedFromPlaylist(self):
        if self.numberOfPlaylist == 0:
            return
        self.numberOfPlaylist -= 1

    def __str__(self):
        return self.getTitle()

    def __eq__(self, other):
        if not isinstance(other, Song):
            return False
        return \
            self.getTitle() == other.getTitle() and \
            self.getAddedDate() == other.getAddedDate() and \
            self.getTimesPlayed() == other.getTimesPlayed() and \
            self.getHoursPlayed() == other.getHoursPlayed() and \
            self.getNumberOfPlaylist() == other.getNumberOfPlaylist()
