import math
import numpy as np
import tkinter as tk
class Canvas(tk.Canvas):
    def __init__(self, root, graph = None):
        super().__init__(root,  bg="#FFFFFF")
        self.place(relx=0.01, rely=0.01,relwidth=0.8, relheight=0.98)
#        self.place(x=0.01, y=0.01, width=1024, height=648)
        
        self.graph = graph
        #  self.zoom = tk.DoubleVar(value=0)
        # self.__zoom_fixed = -100
        # self.__x_rot_fixed = 0
        # self.__y_rot_fixed = 0
        # self.__z_rot_fixed = 0

        # self.x_rot_angle = tk.DoubleVar(value=0)
        # self.y_rot_angle = tk.DoubleVar(value=0)
        # self.z_rot_angle = tk.DoubleVar(value=0)
        self.scale = 50
        # self.position = [0,0]
        self.clipping_z = 20
        
        self.bind("<Configure>", self.setup_centered_coordinates)
        self.setup_centered_coordinates()

#        self.create_oval(0-20, 0-20, 0+20, 0+20, fill= 'blue')

       # print(f"{self.__getitem__('width')=}\n{self.__getitem__('height')=}")
        
   
    def setup_centered_coordinates(self, event=None):
        W = self.winfo_width()
        H = self.winfo_height()
        self.W = W
        self.H = H
        self.configure(scrollregion=(-W/2, -H/2, W/2, H/2))
   #     self.xview_moveto(0.5)
    #    self.yview_moveto(0.5)
#        self.create_oval(-5,-5,5,5,fill='red')

    def implement_controls(self):
       self.selected_vertex = None
       self.__implement_mouse_dragging()
       self.__implement_mouse_scrolling()
       self.__implement_arcball_rotation()


    def __implement_mouse_scrolling(self):
        self.bind("<MouseWheel>", self.on_wheel)  # Windows
        self.bind("<Button-4>", self.on_wheel)   # Linux (scroll up)
        self.bind("<Button-5>", self.on_wheel)   # Linux (scroll down)
    
    
    def __implement_mouse_dragging(self):
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<B1-Motion>",  self.on_motion)
        self.bind("<ButtonRelease-1>", self.on_release)
#        print('mdr')

    def on_release(self, e):
        self.selected_vertex = None

    def on_click(self, e):
#        print(e)
        _x = e.x - self.W/2
        _y = e.y - self.H/2
 #       print(f"{_x=}, {_y=}")
  #      print(f"{self.W=}, {self.H=}")
        closest = self.find_overlapping(_x - 0.5, _y - 0.5, _x + 0.5, _y + 0.5)
        self.selected_vertex = self.graph.vertex_by_id(closest)
        self.click_x = e.x
        self.click_y = e.y

    def on_motion(self, e):
        x, y = e.x, e.y
        self.graph.move_for((x-self.click_x), -(y-self.click_y), self.selected_vertex)
        self.click_x = x
        self.click_y = y


    def on_wheel(self, e):
        if e.num == 4:  # Linux scroll up
            delta = 1.0
        elif e.num == 5:  # Linux scroll down
            delta = -1.0
        else:  # Windows/Mac (<MouseWheel>)
            delta = e.delta
    
        step = -5
        z = delta * step
        self.graph.zoom_for(z, vertex=self.selected_vertex)
    
 #       print(f"Zoom fixed: {self.__zoom_fixed}")

    # def reset_rotation(self):
        # self.x_rot_angle.set(0)
        # self.y_rot_angle.set(0)
        # self.z_rot_angle.set(0)
        #
    # def fix_rotation(self):
        # self.__x_rot_fixed += self.x_rot_angle.get()
        # self.__y_rot_fixed += self.y_rot_angle.get()
        # self.__z_rot_fixed += self.z_rot_angle.get()
        # self.reset_rotation()
        #
        # return [point[0][0], point[1][0], point[2][0]]
        #
    def __implement_arcball_rotation(self):
        self.bind("<Control-ButtonPress-1>", self.start_arcball)
        self.bind("<Control-B1-Motion>", self.drag_arcball)
        self.bind("<Control-ButtonRelease-1>", self.end_arcball)

    def start_arcball(self, event):
        self.ball_x = event.x
        self.ball_y = event.y

    def drag_arcball(self, event):
        if self.ball_x is None:
            return
        x = event.x
        y = event.y
        dx = x - self.ball_x
        dy = y - self.ball_y
        self.ball_x = x
        self.ball_y = y

        rotation_matrix = self.calculate_rotation(dx, dy)
        self.graph.rotate_around_centroid(None,None,None,matrix=rotation_matrix)

    def end_arcball(self, event):
        self.ball_x = None
        self.ball_y = None

    def calculate_rotation(self, dx, dy):
        dy = -dy
        angle = np.sqrt(dx**2 + dy**2) * 0.005  # Angle in radians
        if angle == 0:
            return np.eye(3)  # No rotation

        # Rotation axis (perpendicular to drag direction)
        axis = np.array([dy, -dx, 0])  # y-axis for dx, x-axis for dy, z=0 (screen plane)
        norm = np.linalg.norm(axis)
        if norm == 0:
            return np.eye(3)
        axis = axis / norm

        # Rodrigues' rotation formula
        c = np.cos(angle)
        s = np.sin(angle)
        t = 1 - c
        x, y, z = axis
        rotation_matrix = np.array([
            [t*x*x + c,    t*x*y - z*s, t*x*z + y*s],
            [t*x*y + z*s,  t*y*y + c,   t*y*z - x*s],
            [t*x*z - y*s,  t*y*z + x*s, t*z*z + c]
        ])
        return rotation_matrix

    def project_point(self, x0, y0, z0):
        #_x, _y, _z = self.transform_point(x0, y0, z0)
        if z0 < self.clipping_z:
            #print(f"Point ({x0}, {y0}, {z0}) is behind clipping plane {self.clipping_z}")
            return None, None

        x = x0 * self.clipping_z / z0
        y = y0 * self.clipping_z / z0

        x *= self.scale
        y *= self.scale

        y = -y

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
    



