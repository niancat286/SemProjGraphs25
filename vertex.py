from tkinter import *

class Vertex:
    def __init__(self, x0, y0, z0, number):
        self._x = x0
        self._y = y0
        self._z = z0
        self._number = number

        self.out_edges = []
        self.in_edges = []

        self.screen_x = 0  # координати на канві — оновлюються при рендері
        self.screen_y = 0

        self.canvas_id = None  # id овала вершини на Canvas

    def project_point(self, x0, y0, z0): #ізометричне спотворення
        scale = 40
        screen_x = scale * (x0 - y0)
        screen_y = scale * (x0 + y0) / 2 - scale * z0
        return screen_x + 400, screen_y + 300

    def update_position(self):
        self.screen_x, self.screen_y = self.project_point(self._x, self._y, self._z)

    def move_x(self, x):
        self._x = x
        self.update_position()
    
    def move_y(self, y):
        self._y = y
        self.update_position()

    def move_z(self, z):
        self._z = z
        self.update_position()

    def __str__(self):
        print(f'Vertex {self._number}, cords: {self._x, self._y, self._z}')
