from tkinter import Label, Canvas, Frame
from wavPlayer.constants import ICONS_PATH, GUI_RIGHTSIDE_WIDTH
from PIL.Image import open
from PIL.ImageTk import PhotoImage


class BlinkingButton(Label):
    def __init__(self, master, normal, click, **kw):
        self.normal = normal
        self.click = click

        super().__init__(master, image=self.normal, **kw)
        self.command = lambda *args: print("Working")

        self.bind('<Button-1>', lambda *args: self.clicked())
        self.bind('<ButtonRelease-1>', lambda *args: self.unclicked())

    def setCommand(self, command):
        self.command = command

    def clicked(self):
        self.configure(image=self.click)

    def unclicked(self):
        self.configure(image=self.normal)
        self.command()


class StaticButton(Label):
    def __init__(self, master, normal, click, **kw):
        self.normal = normal
        self.click = click
        self.state = 0

        super().__init__(master, image=self.normal, **kw)
        self.command = lambda *args: print("Working")

        self.bind('<Button-1>', lambda *args: self.clicked())
        self.bind('<ButtonRelease-1>', lambda *args: self.unclicked())

    def setCommand(self, command):
        self.command = command

    def clicked(self):
        if self.state == 0:
            self.configure(image=self.click)
            self.state = 1
        else:
            self.configure(image=self.normal)
            self.state = 0

    def unclicked(self):
        self.command()


class ProgressBar(Canvas):
    def __init__(self, master, width, **kw):
        super().__init__(master, height=4, width=width, bd=0, highlightthickness=0, **kw)
        self.master = master
        self.width = width
        self.progressStep = 1
        self.currentProgress = 0

    def restart(self, seconds):
        self.progressStep = self.width // seconds
        self.delete("all")

    def progress(self):
        x = self.currentProgress
        x2 = x + self.progressStep
        if x2 > self.width:
            x2 = self.width
        self.create_rectangle(x, 0, x2, 4, fill="#6c6c6c", outline="#6c6c6c")
        self.currentProgress = x2
        if x2 == self.width:
            return
        self.master.after(1000, self.progress)


class VolumeBar(Canvas):
    def __init__(self, master):
        super().__init__(master, width=GUI_RIGHTSIDE_WIDTH // 2, height=50, bd=0, highlightthickness=0)
        self.create_rectangle(0, 23, GUI_RIGHTSIDE_WIDTH // 2, 27, fill="#969696", outline="#969696")

        self.ball = self.create_oval(GUI_RIGHTSIDE_WIDTH // 2 - 13, 19, GUI_RIGHTSIDE_WIDTH // 2 - 1, 31,
                                     outline="#7f7f7f", fill="white")

        self.length = GUI_RIGHTSIDE_WIDTH // 2 - 7
        self.x = GUI_RIGHTSIDE_WIDTH // 2 - 7

        self.bind("<B1-Motion>", self.moveBall)

    def moveBall(self, event):
        self.delete(self.ball)
        if event.x < 6:
            event.x = 6
        if event.x > GUI_RIGHTSIDE_WIDTH // 2 - 7:
            event.x = GUI_RIGHTSIDE_WIDTH // 2 - 7
        self.x = event.x

        self.create_rectangle(0, 23, event.x, 27, fill="#969696", outline="#969696")
        self.create_rectangle(event.x, 23, GUI_RIGHTSIDE_WIDTH // 2, 27, fill="#c9c9c9", outline="#c9c9c9")

        self.ball = self.create_oval(event.x - 6, 19, event.x + 6, 31,
                                     outline="#7f7f7f", fill="white")

    def setToZero(self):
        self.delete(self.ball)
        self.x = 6
        self.create_rectangle(6, 23, GUI_RIGHTSIDE_WIDTH // 2, 27, fill="#c9c9c9", outline="#c9c9c9")
        self.ball = self.create_oval(0, 19, 12, 31, outline="#7f7f7f", fill="white")

    def setToMax(self):
        self.delete(self.ball)
        self.x = GUI_RIGHTSIDE_WIDTH // 2 - 7
        self.create_rectangle(0, 23, GUI_RIGHTSIDE_WIDTH // 2 - 7, 27, fill="#969696", outline="#969696")
        self.ball = self.create_oval(GUI_RIGHTSIDE_WIDTH // 2 - 13, 19, GUI_RIGHTSIDE_WIDTH // 2 - 1, 31,
                                     outline="#7f7f7f", fill="white")

    def getVolumePercentage(self) -> float:
        perc = self.x / self.length
        if perc < 0.03:
            return 0
        return perc


class VolumeFrame(Frame):
    def __init__(self, master):
        super().__init__(master, width=GUI_RIGHTSIDE_WIDTH, height=50)
        self.buttonsPhotos = []

        self.lowVolumeButton = self.createBlinkingButton(self, "volume_low")
        self.highVolumeButton = self.createBlinkingButton(self, "volume_high")
        self.volumeBar = VolumeBar(self)

        self.volumeBar.place(relx=0.25)
        self.lowVolumeButton.place(relx=0.19, rely=0.367)
        self.highVolumeButton.place(relx=0.78, rely=0.34)

        self.lowVolumeButton.setCommand(self.volumeBar.setToZero)
        self.highVolumeButton.setCommand(self.volumeBar.setToMax)

    def createBlinkingButton(self, master, name) -> BlinkingButton:
        img = open("{}/{}.png".format(ICONS_PATH, name))
        photo = PhotoImage(img)
        img2 = open("{}/{}_clicked.png".format(ICONS_PATH, name))
        photo2 = PhotoImage(img2)
        self.buttonsPhotos.append(photo)
        self.buttonsPhotos.append(photo2)

        return BlinkingButton(master, photo, photo2, bg="white")


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.geometry("500x260+720+100")

    c = VolumeFrame(root)
    c.pack()

    root.mainloop()
