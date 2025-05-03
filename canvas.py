import tkinter as tk
class Canvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(root,  bg="#FFFFFF")
        self.place(relx=0.01, rely=0.01,relwidth=0.8, relheight=0.9)
                
