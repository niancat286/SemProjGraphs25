from tkinter import *

class Vertex:
    def __init__(self, x0, y0, z0, number, canvas):
        self.x = x0
        self.y = y0
        self.z = z0
        self.r = 20
        self.number = number

        self.out_edges = []
        self.in_edges = []

        self.screen_x = 0  # координати на канві — оновлюються при рендері
        self.screen_y = 0
        
        self.canvas = canvas
        self.canvas_id = None  # id овала вершини на Canvas
        self.label_id = None

    def move_to(self, x0, y0, z0):
        self.x, self.y, self.z = x0, y0, z0
        self.draw()
        
    def draw(self, redraw=1):
        if self.canvas_id is not None:
            self.canvas.delete(self.canvas_id)
            self.canvas.delete(self.label_id)
        self.screen_x, self.screen_y = self.canvas.project_point(self.x, self.y, self.z)

        if redraw:
            for edge in self.out_edges+self.in_edges:
                edge.draw()
        self.canvas_id, self.label_id = self.canvas.draw_circle(self.screen_x, self.screen_y, r = self.r - self.canvas.zoom.get()/40, text = str(self.number))

    def project_point(self, x0, y0, z0): #ізометричне спотворення
        scale = 40
        screen_x = scale * (x0 - y0)
        screen_y = scale * (x0 + y0) / 2 - scale * z0
        return screen_x + 400, screen_y + 300

    def update_position(self):
        self.screen_x, self.screen_y = self.project_point(self._x, self._y, self._z)


   

    def __str__(self):
        print(f'Vertex {self._number}, cords: {self._x, self._y, self._z}')
