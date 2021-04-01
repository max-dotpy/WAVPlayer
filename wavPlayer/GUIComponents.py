from tkinter import Frame, Listbox, Entry
from wavPlayer.MyTkinter import *
from PIL import Image
from PIL.ImageTk import PhotoImage
from wavPlayer.constants import GUI_HEIGHT, GUI_LEFTSIDE_WIDTH, GUI_RIGHTSIDE_WIDTH, ICONS_PATH


def createBlinkingOrStaticButton(cls, master, name, memoryList, **kw) -> BlinkingButton:
    """
        Function that returns a Blinking or Static button, it will be used in the following classes.
    """

    if cls == "blinking":
        img = Image.open("{}/{}.png".format(ICONS_PATH, name))
        img2 = Image.open("{}/{}_clicked.png".format(ICONS_PATH, name))
    else:
        img = Image.open("{}/{}_enabled.png".format(ICONS_PATH, name))
        img2 = Image.open("{}/{}_disabled.png".format(ICONS_PATH, name))
    photo = PhotoImage(img)
    photo2 = PhotoImage(img2)
    memoryList.append(photo)
    memoryList.append(photo2)

    if cls == "blinking":
        return BlinkingButton(master, photo, photo2, **kw)
    return StaticButton(master, photo2, photo, **kw)


class VolumeFrame(Frame):
    """
        This is the Frame containing the Volume functionality and will be implemented later in the class Controls.
    """
    def __init__(self, master):
        super().__init__(master, width=GUI_RIGHTSIDE_WIDTH, height=50)
        self.buttonsPhotos = []

        self.lowVolumeButton = createBlinkingOrStaticButton(
            "blinking", self, "volume_low", self.buttonsPhotos, bg="white")
        self.highVolumeButton = createBlinkingOrStaticButton(
            "blinking", self, "volume_high", self.buttonsPhotos, bg="white")
        self.volumeBar = VolumeBar(self, GUI_RIGHTSIDE_WIDTH // 2)

        self.volumeBar.place(relx=0.25)
        self.lowVolumeButton.place(relx=0.19, rely=0.367)
        self.highVolumeButton.place(relx=0.78, rely=0.34)

        self.lowVolumeButton.setCommand(self.volumeBar.setToZero)
        self.highVolumeButton.setCommand(self.volumeBar.setToMax)


class ButtonsFrame(Frame):
    """
        This is the Frame containing the buttons for interacting with the Music Player
        and will be implemented later in the class Controls.
    """
    def __init__(self, master, width, height, background):
        super().__init__(master, width=width, height=height, bg=background)
        self.buttonsPhotos = []
        self.background = background
        self.displayed = "play"

        self.prevButton = createBlinkingOrStaticButton(
            "blinking", self, "prev", self.buttonsPhotos, bg=self.background)
        self.prevButton.place(relx=0.37, rely=0.3625)

        self.playButton = createBlinkingOrStaticButton(
            "blinking", self, "play", self.buttonsPhotos, bg=self.background)
        self.playButton.place(relx=0.48, rely=0.26)

        self.nextButton = createBlinkingOrStaticButton(
            "blinking", self, "next", self.buttonsPhotos, bg=self.background)
        self.nextButton.place(relx=0.58, rely=0.3625)

        self.pauseButton = createBlinkingOrStaticButton(
            "blinking", self, "pause", self.buttonsPhotos, bg=self.background)

        self.randomButton = createBlinkingOrStaticButton(
            "static", self, "random", self.buttonsPhotos, bg=self.background)
        self.randomButton.place(relx=0.26, rely=0.3625)
        # This sets the "Random shuffle button" to on.
        self.randomButton.setCommand(lambda *args: None)
        self.randomButton.clicked()

        self.reloadButton = createBlinkingOrStaticButton(
            "static", self, "reload", self.buttonsPhotos, bg=self.background)
        self.reloadButton.place(relx=0.70, rely=0.3625)
        # This sets the "Repeat playlist button" to on.
        self.reloadButton.setCommand(lambda *args: None)
        self.reloadButton.clicked()

    def setPrevCommand(self, command):
        self.prevButton.setCommand(command)

    def setPlayCommand(self, command):
        self.playButton.setCommand(command)

    def setNextCommand(self, command):
        self.nextButton.setCommand(command)

    def setPauseCommand(self, command):
        self.pauseButton.setCommand(command)

    def setRandomCommand(self, command):
        self.randomButton.setCommand(command)

    def switchPausePlay(self):
        """
            This method switches between Play Button and Pause Button.
        """

        if self.displayed == "play":
            self.displayed = "pause"
            self.playButton.place_forget()
            self.pauseButton.place(relx=0.48, rely=0.26)
        else:
            self.displayed = "play"
            self.pauseButton.place_forget()
            self.playButton.place(relx=0.48, rely=0.26)
        self.update()


class Table(Frame):
    """
        First piece of the GUI, it contains functionality for choosing Songs, Playlists, searching them, modifying them.
    """
    def __init__(self, master, **kw):
        super().__init__(master, width=GUI_LEFTSIDE_WIDTH, height=GUI_HEIGHT, **kw)

        self.master = master
        self.searchEntry = None
        self.playlistListbox = None
        self.songListbox = None
        self.allSongsListbox = None
        self.plusButton = None
        self.gearButton = None
        self.binButton = None
        self.swap = False

        self.buttonsPhotos = []
        self.currentListbox = "playlist"
        self.listboxKwargs = {"height": 11, "bg": "#c2c2c2", "bd": 0,
                              "selectbackground": "#a6a6a6", "activestyle": "none"}

        self.setLayout()

    def setLayout(self):
        top = Frame(self, width=210, height=30, bg="#c2c2c2")
        top.pack(side="top", fill="both", expand=True)

        self.searchEntry = Entry(top, relief="flat", highlightthickness=0, bg="#a6a6a6")
        self.searchEntry.pack(padx=12, pady=5)

        center = Frame(self, width=210, height=200, bg="#c2c2c2")
        center.pack(side="top", fill="both", expand=True)

        self.playlistListbox = Listbox(center, self.listboxKwargs)
        self.playlistListbox.pack()
        self.playlistListbox.bind("<ButtonRelease-1>", lambda *args: self.playlistClicked())

        self.songListbox = Listbox(center, self.listboxKwargs)
        self.songListbox.bind("<ButtonRelease-1>", lambda *args: self.songClicked())

        self.allSongsListbox = Listbox(center, self.listboxKwargs, selectmode="multiple")

        bot = Frame(self, width=210, height=30, bg="#c2c2c2")
        bot.pack(side="bottom", fill="both", expand=True)

        self.plusButton = createBlinkingOrStaticButton("blinking", bot, "plus", self.buttonsPhotos, bg="#c2c2c2")
        self.plusButton.place(relx=0.28, rely=0.15)
        self.plusButton.setCommand(lambda *args: self.buttonClicked("Add"))

        self.gearButton = createBlinkingOrStaticButton("blinking", bot, "gear", self.buttonsPhotos, bg="#c2c2c2")
        self.gearButton.place(relx=0.43)
        self.gearButton.setCommand(lambda *args: self.buttonClicked("Gear"))

        self.binButton = createBlinkingOrStaticButton("blinking", bot, "bin", self.buttonsPhotos, bg="#c2c2c2")
        self.binButton.place(relx=0.6, rely=0.05)
        self.binButton.setCommand(lambda *args: self.buttonClicked("Bin"))

    def setPlusButtonCommand(self, command):
        self.plusButton.setCommand(command)

    def setGearButtonCommand(self, command):
        self.gearButton.setCommand(command)

    def setBinButtonCommand(self, command):
        self.binButton.setCommand(command)

    def setPlaylistListboxCommand(self, command):
        self.playlistListbox.bind("<ButtonRelease-1>", command)

    def setSongListboxCommand(self, command):
        self.songListbox.bind("<ButtonRelease-1>", command)

    def setReturnEntryCommand(self, command):
        self.searchEntry.bind("<Return>", command)

    def switchListbox(self):
        """
            This method switches between Song and Playlist Listboxes
        """

        if self.currentListbox == "playlist":
            self.playlistListbox.pack_forget()
            self.songListbox.pack()
            self.currentListbox = "song"
            self.setSongListboxCommand(lambda *args: self.songClicked())
        else:
            self.songListbox.pack_forget()
            self.playlistListbox.pack()
            self.currentListbox = "playlist"
            self.setPlaylistListboxCommand(lambda *args: self.playlistClicked())

    def fillPlaylistListbox(self, titles):
        """
            Fills the playlistListbox with the elements of the parameter titles as items.
        """

        self.playlistListbox.delete(0, "end")
        for title in titles:
            self.playlistListbox.insert("end", title)

    def fillSongListbox(self, titles):
        """
            Fills the songListbox with the elements of the parameter titles as items.
        """

        self.songListbox.delete(0, "end")
        for title in titles:
            self.songListbox.insert("end", title)

    def fillAllSongsListbox(self, titles):
        """
            Fills the allSongsListbox with the elements of the parameter titles as items.
        """

        self.allSongsListbox.delete(0, "end")
        for title in titles:
            self.allSongsListbox.insert("end", title)

    def showAllSongsListbox(self):
        """
            This method hides current Listbox and shows allSongsListbox
        """

        if self.currentListbox == "playlist":
            self.playlistListbox.pack_forget()
            self.allSongsListbox.pack()
        else:
            self.songListbox.pack_forget()
            self.allSongsListbox.pack()

    def hideAllSongsListbox(self):
        """
            This method hides allSongsListbox and shows current Listbox
        """

        self.allSongsListbox.pack_forget()
        if self.currentListbox == "playlist":
            self.playlistListbox.pack()
            self.playlistListbox.bind("<ButtonRelease-1>", lambda *args: self.playlistClicked())
        else:
            self.songListbox.pack()
            self.songListbox.bind("<ButtonRelease-1>", lambda *args: self.songClicked())

    def searchListbox(self, complete):
        """
            This methods allows to filter items in the current Listbox showing only strings
            containing the text currently present in the searchEntry.
        """

        text = self.searchEntry.get()
        if text == "":
            if self.currentListbox == "playlist":
                self.fillPlaylistListbox(complete)
            else:
                self.fillSongListbox(complete)
        else:
            lst = [title for title in complete if text.lower() in title.lower()]
            if self.currentListbox == "playlist":
                self.fillPlaylistListbox(lst)
            else:
                self.fillSongListbox(lst)

    def playlistClicked(self):
        self.master.event_generate("<<Playlist clicked>>")

    def songClicked(self):
        self.master.event_generate("<<Song clicked>>")

    def buttonClicked(self, nameOfButton):
        if self.currentListbox == "playlist":
            self.master.event_generate("<<{}Playlist clicked>>".format(nameOfButton))
        else:
            self.master.event_generate("<<{}Song clicked>>".format(nameOfButton))

    def swapSongsOrder(self):
        """
            This method allows to swap the order of 2 items in the current Listbox.
        """

        lst = self.songListbox.curselection()
        if not self.swap:
            self.swap = True
            return
        indexFirst = lst[0]
        indexSecond = lst[1]
        songs = list(self.songListbox.get(0, "end"))
        copy = songs[indexFirst]
        songs[indexFirst] = songs[indexSecond]
        songs[indexSecond] = copy
        self.fillSongListbox(songs)
        self.update()
        self.swap = False


class Controls(Frame):
    """
        Second piece of the GUI, it contains functionality for changing, pausing, unpausing a song, choosing Random and
        Shuffle options, setting the Volume, displaying the current song's title and choosing the option FadeAndExit.
    """

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.titleLabel = None
        self.progressBar = None
        self.buttonsFrame = None
        self.volumeFrame = None
        self.fadeButton = None

        self.setLayout()

    def setLayout(self):
        titleFrame = Frame(self, width=GUI_RIGHTSIDE_WIDTH, height=50)
        titleFrame.pack(fill="y")
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
        bottomFrame.pack(side="bottom", pady=40, padx=170, fill="x")
        self.fadeButton = TextButton(bottomFrame, "#e7e7e7", "#bbbbba", text="Fade and exit")
        self.fadeButton.pack(side="left", padx=30)
        self.fadeButton.setCommand(lambda *args: self.event_generate("<<Fade and exit>>"))

    def setTitleOfSong(self, title):
        """
            Displays the parameter title on the titleLabel.
        """
        self.titleLabel.configure(text="")
        self.titleLabel.update()
        self.titleLabel.configure(text=title)


class GUI:
    """
        This class merges all the previous classes together.
    """

    def __init__(self, master):
        self.table = Table(master)
        self.table.pack(side="left", fill="y")
        self.controls = Controls(master, width=GUI_RIGHTSIDE_WIDTH, height=GUI_HEIGHT)
        self.controls.pack(side="left", fill="y")
