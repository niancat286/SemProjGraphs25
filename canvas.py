import tkinter as tk
class Canvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(root,  bg="#FFFFFF")
        self.place(relx=0.01, rely=0.01,relwidth=0.8, relheight=0.9)
        self.__zoom =30

    @property
    def zoom(self):
        return self.__zoom

    @zoom.setter
    def zoom(self, value):
        self.__zoom = value

    def redraw(self, *args):
        pass
