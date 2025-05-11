import tkinter as tk
import math

class Vertex:
    def __init__(self, x0, y0, z0, number, canvas):
        self.x = x0
        self.y = y0
        self.z = z0
        self.r = 2 #radius
        self.number = number
        self.compare_z = z0-self.r
        self.color = 'paleturquoise2'
        self.t_color = 'black'
        self.out_edges = []
        self.in_edges = []


        #vertex projection is an ellipse inside the rectangle 
        #with opposite vertices: P0(x0, y0) and P1(x1, y1)
        self.P0 = [0, 0]  
        self.P1 = [0, 0]
        self.c = [0,0]
        self.transformed = [0, 0, 0]
        self.canvas = canvas
        self.canvas_id = None  # id овала вершини на Canvas
        self.label_id = None

    def move_to(self, x0, y0, z0):
        self.x, self.y, self.z = x0, y0, z0
#        self.draw()
    def erase(self):
        if self.canvas_id is not None:
            self.canvas.delete(self.canvas_id)
            self.canvas.delete(self.label_id)

    
    def draw(self, redraw=0):

        self.erase()
        if redraw:
            self.calc_projection()
            for edge in self.out_edges+self.in_edges:
                edge.draw()

        if(self.P0[0] == None):
            self.canvas_id = self.label_id = None
            return
#        print(*self.P0)
#        print(*self.P1)
#        print(self.P0)
#        print(self.P1)
        self.canvas_id = self.canvas.create_oval(*self.P0, *self.P1, fill = self.color, outline = self.color)
        self.label_id = self.canvas.create_text(self.c[0], self.c[1], text = self.number, fill = self.t_color, anchor = 'center')

        #self.label_id = self.canvas.draw_circle(self.screen_x, self.screen_y, r = self.r - self.canvas.zoom.get()/40, text = str(self.number))
        #self.canvas.draw_circle(*self.canvas.project_point2(self.x, self.y, self.z), r = self.r - self.canvas.zoom.get()/40, text = str(self.number), color='pink')
    

    def calc_projection(self):
        self.transformed  = self.canvas.transform_point(self.x, self.y, self.z)
        x0, y0, z0 = self.transformed
        self.compare_z = z0-self.r

        eps = 0.001
        r = self.r
        scale = self.canvas.scale
        if z0 + r + eps < self.canvas.clipping_z:
            #vertex is fully outside projectable zone
            self.P0 = [None, None]
            return
        elif z0 < self.canvas.clipping_z:
            #vertex is partially inside projectable zone
            _r = (r**2 - (self.canvas.clipping_z - z0)**2)**(1/2)
            _r *= scale
            x,y = self.canvas.project_point(x0,y0,self.canvas.clipping_z)
            #wrong, has to be calculated
            self.c = [x,y]
            self.P0 = [x-_r, y-_r]
            self.P1 = [x+_r, y+_r]
        else:
            #vertex is fully inside projectable zone 
            #may be wrong
            z1 = self.canvas.clipping_z
            if (x0 == 0 and y0 == 0):
                t = (z1 * r)/((z0**2 - r**2)**(1/2))
                self.c = [0,0]
                self.P0 = [t*scale, t*scale]
                self.P1 = [-t*scale, -t*scale]

                return
            a = z1*r*((x0**2 + y0**2 + z0**2 - r**2)**(1/2)) / (z0**2 - r**2)
            b = z1*r / ((x0**2 + y0**2 + z0**2 - r**2)**(1/2))
            t1 = z1*x0/z0
            t2 = (((a**2) * (x0**2) + (b**2) * (y0**2))/(x0**2 + y0**2))**(1/2)
            t3 = z1*y0/z0
            self.c = [z1*x0/z0, -(z1*y0/z0)]
            self.P0 = [t1+t2, -(t3+t2)]
            self.P1 = [t1-t2, -(t3-t2)]

            self.c[0] *= scale
            self.c[1] *= scale
            self.P0[0] *= scale
            self.P0[1] *= scale
            self.P1[0] *= scale
            self.P1[1] *= scale




    def update_position(self):
        self.screen_x, self.screen_y = self.project_point(self._x, self._y, self._z)


   

    def __str__(self):
        print(f'Vertex {self._number}, cords: {self._x, self._y, self._z}')
