class Playlist:
    def __init__(self, title, creationDate, timesPlayed=0, hoursPlayed=0, songs=None, firstSong=None, changesRecord=""):
        self.title = title
        self.creationDate = creationDate
        self.timesPlayed = timesPlayed
        self.hoursPlayed = hoursPlayed
        self.songs = [] if songs is None else songs
        self.firstSong = {} if firstSong is None else firstSong
        self.changesRecord = changesRecord

    def getTitle(self):
        return self.title

    def getCreationDate(self):
        return self.creationDate

    def getTimesPlayed(self):
        return self.timesPlayed

    def getHoursPlayed(self):
        return self.hoursPlayed

    def getSongs(self):
        return self.songs

    def getNumberOfSongs(self):
        return len(self.songs)

    def getFirstSong(self):
        return self.firstSong

    def getChangesRecord(self):
        return self.changesRecord

    def played(self):
        self.timesPlayed += 1

    def playedFor(self, minutes):
        self.hoursPlayed += minutes / 60

    def firstSongPicked(self, song):
        if song in self.firstSong:
            self.firstSong[song] += 1
        else:
            self.firstSong[song] = 1

    def addChanges(self, sign, title):
        self.changesRecord += "{} {}\n".format(sign, title)

    def addSong(self, song):
        self.songs.append(song)
        self.addChanges("+", song.getTitle())

    def removeSong(self, song):
        del self.songs[self.songs.index(song)]
        self.addChanges("-", song.getTitle())
