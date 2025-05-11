import math
import tkinter as tk

class Edge:
    def __init__(self, vertex1, vertex2, edge_id, canvas):
        self.__v1 = vertex1
        self.__v2 = vertex2
        self.ids = [*edge_id]

        self.canvas = canvas
        self.canvas_id = None  # id лінії
        self.label_id = None  # id тексту

    def draw(self):
        if self.canvas_id is not None:
            self.canvas.delete(self.canvas_id)
            #self.canvas.delete(self.label_id)
        x0, y0, z0 = self.__v1.transformed
        x1, y1, z1 = self.__v2.transformed 

        r = self.__v1.r
        u = [x1-x0, y1-y0, z1-z0]
        dist = (u[0]**2 + u[1]**2 + u[2]**2 ) ** (1/2)
        if(dist < r * 2):
            drawn = 1
            self.canvas_id = None
            self.label_id  = None
            return
        u = [u[0]/dist, u[1]/dist, u[2]/dist]
        eps = 0.0001
        A = [x0+(r * u[0])-eps, y0+(r*u[1])-eps, z0+(r*u[2])-eps]
        B = [x1-(r * u[0]), y1-(r*u[1]), z1-(r*u[2])]
        if(A[2] < self.canvas.clipping_z and B[2] < self.canvas.clipping_z):
            return
        arrow = 'last'
        _V1 = A
        _V2 = B
        if(B[2] < self.canvas.clipping_z or A[2] < self.canvas.clipping_z):
            t = (self.canvas.clipping_z - A[2])/(B[2]-A[2])
            x = A[0] + t*(B[0]-A[0])
            y = A[1] + t*(B[0]-A[0])
            if(B[2] < self.canvas.clipping_z):
                _V1 = [A[0], A[1], A[2]]
                _V2 = [x,y,20]
                arrow = None
            else:
                _V1 = [x,y,20]
                _V2 = [B[0], B[1], B[2]]

        x0, y0 = self.canvas.project_point(*_V1)
        x1, y1 = self.canvas.project_point(*_V2)
        if(x0 == None):
            print('THIS WAS NOT SUPPOSSED TO HAPPEN')
            raise Exception
        self.canvas_id = self.canvas.create_line(x0, y0, x1, y1, fill='blue', arrow = arrow)

    def add_paralel(self, edge_id):
        self.ids.append(edge_id)
