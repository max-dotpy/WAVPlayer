from tkinter import Label


class blinkingButton(Label):
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


class staticButton(Label):
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
