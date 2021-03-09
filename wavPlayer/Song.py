class Song:
    def __init__(self, title, addedDate, timesPlayed=0, hoursPlayed=0, numberOfPlaylist=0):
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

    def played(self):
        self.timesPlayed += 1

    def playedFor(self, minutes):
        self.hoursPlayed += minutes / 60

    def addedToPlaylist(self):
        self.numberOfPlaylist += 1

    def removedFromPlaylist(self):
        if self.numberOfPlaylist == 0:
            raise MemoryError
        self.numberOfPlaylist -= 1

    def getData(self) -> dict:
        return {"Added date": self.getAddedDate(),
                "Number of times played": self.getTimesPlayed(),
                "Number of hours played": self.getHoursPlayed(),
                "Number of playlist it is in": self.getNumberOfPlaylist()}

    def __str__(self):
        return self.getTitle()
