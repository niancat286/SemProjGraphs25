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

    def draw_line(self, x0, y0, x1, y1, width=1, color='blue'):
        self.create_line(x0,y0, x1,y1, width=width, fill=color)


    def draw_circle(self, x, y, r=10, color='lightred', text=None, text_color='black'):
        canvas.create_oval(
            x - r, y - r,
            x + r, y + r,
            fill = point_color,
            outline=''
        )
        if(text == None):
            return
        canvas.create_text(
            x, y,
            text = text,
            fill = text_color,
            anchor = 'center'
        )






    def move_up(self):
        self.position[1] -= 10
        self.reposition()

    def move_down(self):
        self.position[1] += 10
        self.reposition()

    def move_right(self):
        self.position[0] += 10
        self.reposition()

    def move_left(self):
        self.position[0] -= 10
        self.reposition()

    def reposition(self):
        self.scan_mark(0,0)
        self.scan_dragto(*self.position)


    def redraw(self, *args):
        print(f"{self.zoom.get()=}\n{self.x_rot_angle.get()=}\n{self.y_rot_angle.get()=}\n{self.z_rot_angle.get()=}")
        pass
