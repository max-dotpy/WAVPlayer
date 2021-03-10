from tkinter import *
from wavPlayer.MyTkinter import blinkingButton, staticButton
from PIL.Image import open
from PIL.ImageTk import PhotoImage
from wavPlayer.constants import GUI_HEIGHT, GUI_LEFTSIDE_WIDTH, GUI_WIDTH, ICONS_PATH


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

    def createBlinkingButton(self, master, name) -> blinkingButton:
        img = open("{}/{}.png".format(ICONS_PATH, name))
        photo = PhotoImage(img)
        img2 = open("{}/{}_clicked.png".format(ICONS_PATH, name))
        photo2 = PhotoImage(img2)
        self.buttonsPhotos.append(photo)
        self.buttonsPhotos.append(photo2)

        return blinkingButton(master, photo, photo2, bg="#c2c2c2")

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


if __name__ == '__main__':
    root = Tk()
    root.geometry("860x260+720+100")

    table = Table(root)
    table.pack(side=LEFT, fill=Y)

    root.mainloop()
