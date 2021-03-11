from tkinter import *
from wavPlayer.MyTkinter import BlinkingButton, ProgressBar, VolumeFrame, ButtonsFrame, TextButton
from PIL.Image import open
from PIL.ImageTk import PhotoImage
from wavPlayer.constants import GUI_HEIGHT, GUI_LEFTSIDE_WIDTH, GUI_RIGHTSIDE_WIDTH, ICONS_PATH


class Table(Frame):
    """
    methods:
    + setLayout
    + createBlinkingButton
    + setPlusButtonCommand
    + setGearButtonCommand
    + setBinButtonCommand
    + switchListbox
    + fillPlaylistListbox
    + fillSongListbox
    + setPlaylistsDict
    + setMusicPlayer
    + setRandomButton
    + setReloadButton
    + setReturnEntryCommand
    + searchPlaylistListbox
    + searchSongListbox
    + setCurrentPlaylistsTitles
    + setCurrentSongsTitles
    + setCurrentPlaylist
    + playlistClicked
    + songClicked
    """
    def __init__(self, master, **kw):
        super().__init__(master, width=GUI_LEFTSIDE_WIDTH, height=GUI_HEIGHT, **kw)

        self.master = master
        self.searchEntry = None
        self.playlistListbox = None
        self.songListbox = None
        self.plusButton = None
        self.gearButton = None
        self.binButton = None

        self.buttonsPhotos = []
        self.currentListbox = "playlist"
        self.currentPlaylistsTitles = []
        self.currentSongsTitles = []
        self.currentPlaylist = None
        self.playlistsDict = None
        self.musicPlayer = None
        self.reloadButton = None
        self.randomButton = None
        self.setLayout()

    def setLayout(self):
        top = Frame(self, width=210, height=30, bg="#c2c2c2")
        top.pack(side=TOP, fill=BOTH, expand=True)

        self.searchEntry = Entry(top, relief=FLAT, highlightthickness=0, bg="#a6a6a6")
        self.searchEntry.pack(padx=12, pady=5)

        center = Frame(self, width=210, height=200, bg="#c2c2c2")
        center.pack(side=TOP, fill=BOTH, expand=True)

        self.playlistListbox = Listbox(center, height=11, bg="#c2c2c2", bd=0, selectbackground="#a6a6a6",
                                       activestyle=NONE)
        self.playlistListbox.pack()
        self.playlistListbox.bind("<ButtonRelease-1>", lambda *args: self.playlistClicked())

        self.songListbox = Listbox(center, height=11, bg="#c2c2c2", bd=0, selectbackground="#a6a6a6",
                                   activestyle=NONE)

        self.songListbox.bind("<ButtonRelease-1>", lambda *args: self.songClicked(
            self.randomButton.getState(), self.reloadButton.getState()))

        bot = Frame(self, width=210, height=30, bg="#c2c2c2")
        bot.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.plusButton = self.createBlinkingButton(bot, "plus")
        self.plusButton.place(relx=0.28, rely=0.15)

        self.gearButton = self.createBlinkingButton(bot, "gear")
        self.gearButton.place(relx=0.43)

        self.binButton = self.createBlinkingButton(bot, "bin")
        self.binButton.place(relx=0.6, rely=0.05)

        self.setReturnEntryCommand(lambda *args: self.searchPlaylistListbox())

    def createBlinkingButton(self, master, name) -> BlinkingButton:
        img = open("{}/{}.png".format(ICONS_PATH, name))
        photo = PhotoImage(img)
        img2 = open("{}/{}_clicked.png".format(ICONS_PATH, name))
        photo2 = PhotoImage(img2)
        self.buttonsPhotos.append(photo)
        self.buttonsPhotos.append(photo2)

        return BlinkingButton(master, photo, photo2, bg="#c2c2c2")

    def setPlusButtonCommand(self, command):
        self.plusButton.setCommand(command)

    def setGearButtonCommand(self, command):
        self.gearButton.setCommand(command)

    def setBinButtonCommand(self, command):
        self.binButton.setCommand(command)

    def switchListbox(self):
        if self.currentListbox == "playlist":
            self.playlistListbox.pack_forget()
            self.songListbox.pack()
            self.currentListbox = "song"
            self.setReturnEntryCommand(lambda *args: self.searchSongListbox())
        else:
            self.songListbox.pack_forget()
            self.playlistListbox.pack()
            self.currentListbox = "playlist"
            self.setReturnEntryCommand(lambda *args: self.searchPlaylistListbox())

    def fillPlaylistListbox(self, titles):
        self.playlistListbox.delete(0, END)
        for title in titles:
            self.playlistListbox.insert(END, title)

    def fillSongListbox(self, titles):
        self.songListbox.delete(0, END)
        for title in titles:
            self.songListbox.insert(END, title)

    def setPlaylistsDict(self, dictionary):
        self.playlistsDict = dictionary

    def setMusicPlayer(self, musicPlayer):
        self.musicPlayer = musicPlayer

    def setRandomButton(self, button):
        self.randomButton = button

    def setReloadButton(self, button):
        self.reloadButton = button

    def setReturnEntryCommand(self, command):
        self.searchEntry.bind("<Return>", command)

    def searchPlaylistListbox(self):
        text = self.searchEntry.get()
        if text == "":
            self.fillPlaylistListbox(self.currentPlaylistsTitles)
        else:
            lst = [title for title in self.currentPlaylistsTitles if text.lower() in title.lower()]
            self.fillPlaylistListbox(lst)

    def searchSongListbox(self):
        text = self.searchEntry.get()
        if text == "":
            self.fillSongListbox(self.currentSongsTitles)
        else:
            lst = [title for title in self.currentSongsTitles if text.lower() in title.lower()]
            self.fillSongListbox(lst)

    def setCurrentPlaylistsTitles(self, titles):
        self.currentPlaylistsTitles = titles

    def setCurrentSongsTitles(self, titles):
        self.currentSongsTitles = titles

    def setCurrentPlaylist(self, playlist):
        self.currentPlaylist = playlist

    def playlistClicked(self):
        index = self.playlistListbox.curselection()[0]
        title = self.currentPlaylistsTitles[index]
        songs = self.playlistsDict[title].getSongsTitles()
        self.fillSongListbox(songs)
        self.setCurrentSongsTitles(songs)
        self.setCurrentPlaylist(self.playlistsDict[title])
        self.switchListbox()

        self.playlistsDict[title].played()

    def songClicked(self, randomState, reloadState):
        index = self.songListbox.curselection()[0]
        title = self.currentSongsTitles[index]
        song = self.currentPlaylist.getSongFromTitle(title)

        # TODO: ok abbiamo la first song, crea la playlist, a seconda del reload e del random,
        # TODO: e poi salva tutti i dati e fai partire

        if randomState:
            pass
        else:
            order = self.currentPlaylist.getOrderedPlaylist()


class Controls(Frame):
    """
    methods:
    + setLayout
    + statisticsCommand
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.titleLabel = None
        self.progressBar = None
        self.buttonsFrame = None
        self.volumeFrame = None
        self.fadeButton = None
        self.statisticsButton = None

        self.setLayout()

    def setLayout(self):
        titleFrame = Frame(self, width=GUI_RIGHTSIDE_WIDTH, height=50)
        titleFrame.pack(fill=Y)
        titleFrame.pack_propagate(0)

        self.titleLabel = Label(titleFrame, bd=0)
        self.titleLabel.pack(pady=15)

        self.progressBar = ProgressBar(self, GUI_RIGHTSIDE_WIDTH, bg="#d0d0d0")
        self.progressBar.pack()

        self.buttonsFrame = ButtonsFrame(self, GUI_RIGHTSIDE_WIDTH, 40, "white")
        self.buttonsFrame.pack()

        self.volumeFrame = VolumeFrame(self)
        self.volumeFrame.pack()

        bottomFrame = Frame(self)
        bottomFrame.pack(side=BOTTOM, pady=40, padx=150, fill=X)
        self.fadeButton = TextButton(bottomFrame, "#e7e7e7", "#bbbbba", text="Fade and exit")
        self.fadeButton.pack(side=LEFT, padx=10)
        self.statisticsButton = TextButton(bottomFrame, "#e7e7e7", "#bbbbba", text="Statistics")
        self.statisticsButton.pack(side=LEFT)

    # TODO: implement this
    def statisticsCommand(self):
        pass


class GUI:
    """
    methods:
    + getTable
    + getControls
    """
    def __init__(self, master):
        self.table = Table(master)
        self.table.pack(side=LEFT, fill=Y)
        self.controls = Controls(master, width=GUI_RIGHTSIDE_WIDTH, height=GUI_HEIGHT)
        self.controls.pack(side=LEFT, fill=Y)

    def getTable(self) -> Table:
        return self.table

    def getControls(self) -> Controls:
        return self.controls


if __name__ == '__main__':
    root = Tk()
    root.geometry("710x260+720+100")
    root.title("")

    gui = GUI(root)

    root.mainloop()
