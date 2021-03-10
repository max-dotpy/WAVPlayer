from tkinter import *
from wavPlayer.MyTkinter import BlinkingButton, StaticButton, ProgressBar, VolumeFrame
from PIL.Image import open
from PIL.ImageTk import PhotoImage
from wavPlayer.constants import GUI_HEIGHT, GUI_LEFTSIDE_WIDTH, GUI_WIDTH, GUI_RIGHTSIDE_WIDTH, ICONS_PATH


class Table(Frame):
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

        self.songListbox = Listbox(center, height=11, bg="#c2c2c2", bd=0, selectbackground="#a6a6a6",
                                   activestyle=NONE)

        bot = Frame(self, width=210, height=30, bg="#c2c2c2")
        bot.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.plusButton = self.createBlinkingButton(bot, "plus")
        self.plusButton.place(relx=0.28, rely=0.15)

        self.gearButton = self.createBlinkingButton(bot, "gear")
        self.gearButton.place(relx=0.43)

        self.binButton = self.createBlinkingButton(bot, "bin")
        self.binButton.place(relx=0.6, rely=0.05)

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
        else:
            self.songListbox.pack_forget()
            self.playlistListbox.pack()
            self.currentListbox = "playlist"

    def fillPlaylistListbox(self, titles):
        self.playlistListbox.delete(0, END)
        for title in titles:
            self.playlistListbox.insert(END, title)

    def fillSongListbox(self, titles):
        self.songListbox.delete(0, END)
        for title in titles:
            self.songListbox.insert(END, title)

    def setReturnEntryCommand(self, command):
        self.searchEntry.bind("<Return>", command)


class Controls(Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)


class ButtonsFrame(Frame):
    def __init__(self, master, width, height, background):
        super().__init__(master, width=width, height=height, bg=background)
        self.buttonsPhotos = []
        self.background = background

        self.prevButton = self.createBlinkingButton("prev")
        self.prevButton.place(relx=0.37, rely=0.3625)

        self.playButton = self.createBlinkingButton("play")
        self.playButton.place(relx=0.48, rely=0.26)

        self.nextButton = self.createBlinkingButton("next")
        self.nextButton.place(relx=0.58, rely=0.3625)

        self.pauseButton = self.createBlinkingButton("pause")
        # self.pauseButton.place(relx=0.48, rely=0.26)

        self.randomButton = self.createStaticButton("random")
        self.randomButton.place(relx=0.26, rely=0.3625)

        self.reloadButton = self.createStaticButton("reload")
        self.reloadButton.place(relx=0.70, rely=0.3625)

    def createBlinkingButton(self, name) -> BlinkingButton:
        img = open("{}/{}.png".format(ICONS_PATH, name))
        photo = PhotoImage(img)
        img2 = open("{}/{}_clicked.png".format(ICONS_PATH, name))
        photo2 = PhotoImage(img2)
        self.buttonsPhotos.append(photo)
        self.buttonsPhotos.append(photo2)

        return BlinkingButton(self, photo, photo2, bg=self.background)

    def createStaticButton(self, name) -> StaticButton:
        img = open("{}/{}_enabled.png".format(ICONS_PATH, name))
        photo = PhotoImage(img)
        img2 = open("{}/{}_disabled.png".format(ICONS_PATH, name))
        photo2 = PhotoImage(img2)
        self.buttonsPhotos.append(photo)
        self.buttonsPhotos.append(photo2)

        return StaticButton(self, photo2, photo, bg=self.background)

    def setRandomCommand(self, command):
        self.randomButton.setCommand(command)

    def setPrevCommand(self, command):
        self.prevButton.setCommand(command)

    def setPlayCommand(self, command):
        self.playButton.setCommand(command)

    def setNextCommand(self, command):
        self.nextButton.setCommand(command)

    def setReloadCommand(self, command):
        self.reloadButton.setCommand(command)

    def setPauseCommand(self, command):
        self.pauseButton.setCommand(command)


if __name__ == '__main__':
    root = Tk()
    root.geometry("710x260+720+100")
    root.title("")

    table = Table(root)
    table.pack(side=LEFT, fill=Y)

    controls = Controls(root, width=GUI_RIGHTSIDE_WIDTH, height=260)
    controls.pack(side=LEFT, fill=Y)

    titleFrame = Frame(controls, width=GUI_RIGHTSIDE_WIDTH, height=50)
    titleFrame.pack(fill=Y)
    titleFrame.pack_propagate(0)

    titleLabel = Label(titleFrame, text="Titolo canzone", bd=0)
    titleLabel.pack(pady=15)

    bar = ProgressBar(controls, GUI_RIGHTSIDE_WIDTH, bg="#d0d0d0")
    bar.pack()
    bar.restart(120)
    bar.progress()

    buttonsFrame = ButtonsFrame(controls, GUI_RIGHTSIDE_WIDTH, 40, "white")
    buttonsFrame.pack()

    volumeFrame = VolumeFrame(controls)
    volumeFrame.pack()

    root.mainloop()
