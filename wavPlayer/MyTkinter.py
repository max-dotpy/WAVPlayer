from tkinter import Label, Canvas


class BlinkingButton(Label):
    """
        This is an image button that changes image when clicked. When the click is released the
        image changes back and the command runs.
    """
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


class StaticButton(BlinkingButton):
    """
        This is an image button that changes image when clicked. When the click is released the
        image doesn't change back and the command runs. The image changes back when clicked a second time.
    """
    def __init__(self, master, normal, click, **kw):
        super().__init__(master, normal, click, **kw)
        self.state = 0

    def clicked(self):
        if self.state:
            self.configure(image=self.normal)
            self.state = 0
        else:
            self.configure(image=self.click)
            self.state = 1

    def unclicked(self):
        self.command()

    def getState(self) -> bool:
        if self.state:
            return True
        return False


class TextButton(Label):
    """
        This is a text button that changes background color when clicked.
        It changes back and run its command when unclicked.
    """
    def __init__(self, master, background, backgroundClicked, **kw):
        super().__init__(master, bg=background, **kw)

        self.background = background
        self.backgroundClicked = backgroundClicked

        self.command = lambda *args: print("Working")

        self.bind('<Button-1>', lambda *args: self.clicked())
        self.bind('<ButtonRelease-1>', lambda *args: self.unclicked())

    def setCommand(self, command):
        self.command = command

    def clicked(self):
        self.configure(bg=self.backgroundClicked)

    def unclicked(self):
        self.configure(bg=self.background)
        self.command()


class ProgressBar(Canvas):
    """
        A simple progress bar that progresses when the progress method is called.
    """
    def __init__(self, master, width, color="#6c6c6c", **kw):
        super().__init__(master, height=4, width=width, bd=0, highlightthickness=0, **kw)
        self.master = master
        self.width = width
        self.color = color

    def restart(self):
        self.delete("all")

    def progress(self, percentage):
        x = int(self.width * percentage)
        self.create_rectangle(0, 0, x, 4, fill=self.color, outline=self.color)


class VolumeBar(Canvas):
    def __init__(self, master, width, ballOutline="#7f7f7f", ballFill="white", dark="#969696", light="#c9c9c9", **kw):
        super().__init__(master, width=width, height=50, bd=0, highlightthickness=0, **kw)
        self.master = master
        self.width = width
        self.ballOutline = ballOutline
        self.ballFill = ballFill
        self.dark = dark
        self.light = light

        self.ball = None
        self.length = width - 7
        self.x = width - 7

        # The volume is at first set to Max.
        self.setToMax()
        self.bind("<B1-Motion>", self.moveBall)

    def drawBall(self, x1, x2):
        self.ball = self.create_oval(x1, 19, x2, 31, outline=self.ballOutline, fill=self.ballFill)

    def moveBall(self, event):
        self.delete(self.ball)
        if event.x < 6:
            event.x = 6
        if event.x > self.width - 7:
            event.x = self.width - 7
        self.x = event.x
        self.create_rectangle(0, 23, event.x, 27, fill=self.dark, outline=self.dark)
        self.create_rectangle(event.x, 23, self.width, 27, fill=self.light, outline=self.light)
        self.drawBall(event.x - 6, event.x + 6)
        self.event_generate("<<Volume changed>>")

    def setToZero(self):
        self.delete(self.ball)
        self.x = 6
        self.create_rectangle(6, 23, self.width, 27, fill=self.light, outline=self.light)
        self.drawBall(0, 12)
        self.event_generate("<<Volume changed>>")

    def setToMax(self):
        self.delete(self.ball)
        self.x = self.width - 7
        self.create_rectangle(0, 23, self.width - 7, 27, fill=self.dark, outline=self.dark)
        self.drawBall(self.width - 13, self.width - 1)
        self.event_generate("<<Volume changed>>")

    def getVolumePercentage(self) -> float:
        perc = self.x / self.length
        if perc < 0.03:
            return 0
        return perc
