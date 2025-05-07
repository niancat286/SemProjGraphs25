import tkinter as tk
class Canvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(root,  bg="#FFFFFF")
        self.place(relx=0.01, rely=0.01,relwidth=0.8, relheight=0.9)
        self.zoom = tk.DoubleVar(value=30)
        self.x_rot_angle = tk.DoubleVar(value=0)
        self.y_rot_angle = tk.DoubleVar(value=0)
        self.z_rot_angle = tk.DoubleVar(value=0)
        
        self.position = [0,0]

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_right(self):
        pass

    def move_left(self):
        pass

    def redraw(self, *args):
        print(f"{self.zoom.get()=}\n{self.x_rot_angle.get()=}\n{self.y_rot_angle.get()=}\n{self.z_rot_angle.get()=}")
        pass
