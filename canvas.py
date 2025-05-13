import math
import numpy as np
import tkinter as tk
class Canvas(tk.Canvas):
    def __init__(self, root):
        super().__init__(root,  bg="#FFFFFF")
        self.place(relx=0.01, rely=0.01,relwidth=0.8, relheight=0.9)
#        self.place(x=0.01, y=0.01, width=1024, height=648)
        

        self.__implement_mouse_dragging()

        self.zoom = tk.DoubleVar(value=50)
        
        self.__x_rot_fixed = 0
        self.__y_rot_fixed = 0
        self.__z_rot_fixed = 0

        self.x_rot_angle = tk.DoubleVar(value=0)
        self.y_rot_angle = tk.DoubleVar(value=0)
        self.z_rot_angle = tk.DoubleVar(value=0)
        self.scale = 1000
        self.position = [0,0]

        print(f"{self.__getitem__('width')=}\n{self.__getitem__('height')=}")

    def __implement_mouse_dragging(self):
        self.bind("<ButtonPress-1>", lambda e: self.scan_mark(e.x, e.y))
        self.bind("<B1-Motion>",    lambda e: self.scan_dragto(e.x, e.y, gain=1))



    def draw_line(self, x0, y0, x1, y1, width=1, color='blue'):
        #cx = x1 + (x1 + x0) / 2
        #cy = y1 - (y1 - y0)/2
        return self.create_line(x0,y0,x1,y1, width=width, fill=color, arrow=tk.LAST)
        #return self.create_line(x0,y0, cx, cy, x1,y1, width=width, fill=color, arrow=tk.LAST, smooth=True)


    def draw_circle(self, x, y, r=10, color='paleturquoise2', text=None, text_color='black'):
        point = self.create_oval(
            x - r, y - r,
            x + r, y + r,
            fill = color,
            outline=''
        )
        if(text == None):
            return
        label = self.create_text(
            x, y,
            text = text,
            fill = text_color,
            anchor = 'center'
        )
        return point, label


    def reset_rotation(self, *args):
        self.x_rot_angle.set(0)
        self.y_rot_angle.set(0)
        self.z_rot_angle.set(0)

    def fix_rotation(self, *args):
        self.__x_rot_fixed += self.x_rot_angle.get()
        self.__y_rot_fixed += self.y_rot_angle.get()
        self.__z_rot_fixed += self.z_rot_angle.get()
        self.reset_rotation()



    def move_up(self, step=1):
        self.scan_mark(0,0)
        self.scan_dragto(self.position[0], self.position[1]-step)

    def move_down(self, step=1):
        self.scan_mark(0,0)
        self.scan_dragto(self.position[0], self.position[1]+step)

    def move_right(self, step=1):
        self.scan_mark(0,0)
        self.scan_dragto(self.position[0]+step, self.position[1])

    def move_left(self, step=1):
        self.scan_mark(0,0)
        self.scan_dragto(self.position[0]-step, self.position[1])


    def project_point(self, x0, y0, z0):
        point = [[x0], [y0], [z0]]
    #    print(f"{point=} , {rotation_x=} {rotation_y=} {rotation_z=} {zoom=}")
    
        rotation_x, rotation_y, rotation_z = self.calculate_matrices()

        rotated_2d = np.matmul(rotation_y, point)
        rotated_2d = np.matmul(rotation_x, rotated_2d)
        rotated_2d = np.matmul(rotation_z, rotated_2d)
    
        z = 1/(self.zoom.get() - rotated_2d[2][0])
        projection_matrix = [[z, 0, 0],
                            [0, z, 0]]
        projected_2d = np.matmul(projection_matrix, rotated_2d)
        x = int(projected_2d[0][0] * self.scale)
        #The (-) sign in the Y is because the canvas' Y axis starts  from Top to Bottom
        y = -int(projected_2d[1][0] * self.scale)

        return x, y
   
    def __simplify_angle(self, angle_fixed, angle):
        PI_2 = 6.283185307
        angle = angle_fixed + angle
        k = -1 if angle < 0 else 1
        angle = abs(angle)
        while(angle > PI_2):
            angle -= PI_2
        return angle * k 

    def calculate_matrices(self):
        angle_x = self.__simplify_angle(self.__x_rot_fixed, self.x_rot_angle.get())
        angle_y = self.__simplify_angle(self.__y_rot_fixed, self.y_rot_angle.get())
        angle_z = self.__simplify_angle(self.__z_rot_fixed, self.z_rot_angle.get())

        rotation_x =    [[1, 0, 0],
                        [0, math.cos(angle_x), -math.sin(angle_x)],
                        [0, math.sin(angle_x), math.cos(angle_x)]]
    
        rotation_y =    [[math.cos(angle_y), 0, -math.sin(angle_y)],
                        [0, 1, 0],
                        [math.sin(angle_y), 0, math.cos(angle_y)]]
    
        rotation_z =    [[math.cos(angle_z), -math.sin(angle_z), 0],
                        [math.sin(angle_z), math.cos(angle_z), 0],
                        [0, 0 ,1]]
        return rotation_x, rotation_y, rotation_z
    



    def redraw(self, *args):
        print(f"{self.zoom.get()=}\n{self.x_rot_angle.get()=}\n{self.y_rot_angle.get()=}\n{self.z_rot_angle.get()=}")
        pass
