class Song:
    def __init__(self, title, addedDate, timesPlayed=0, hoursPlayed=0, numberOfPlaylist=0):
        self.title = title
        self.addedDate = addedDate
        self.timesPlayed = timesPlayed
        self.hoursPlayed = hoursPlayed
        self.numberOfPlaylist = numberOfPlaylist

    def getTitle(self):
        return self.title

    def getAddedDate(self):
        return self.addedDate

    def getTimesPlayed(self):
        return self.timesPlayed

    def getHoursPlayed(self):
        return self.hoursPlayed

    def getNumberOfPlaylist(self):
        return self.numberOfPlaylist

    def played(self):
        self.timesPlayed += 1

    def playedFor(self, minutes):
        self.hoursPlayed += minutes / 60

    def addedToPlaylist(self):
        self.numberOfPlaylist += 1

    def removedFromPlaylist(self):
        if self.numberOfPlaylist == 0:
            raise RuntimeError
        self.numberOfPlaylist -= 1

