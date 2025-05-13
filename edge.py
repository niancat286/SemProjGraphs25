import math
import tkinter as tk

class Edge:
    def __init__(self, vertex1, vertex2, edge_id, canvas):
        self.__v1 = vertex1
        self.__v2 = vertex2
        self.ids = edge_id

        self.canvas = canvas
        self.canvas_id = None  # id лінії
        self.label_id = None  # id тексту

    def draw(self):
        if self.canvas_id is not None:
            self.canvas.delete(self.canvas_id)
            self.canvas.delete(self.label_id)
        x0, y0 = self.__v1.screen_x, self.__v1.screen_y
        x1, y1 = self.__v2.screen_x, self.__v2.screen_y

        dx = x1 - x0
        dy = y1 - y0
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist == 0:
            return
        r = self.__v1.r - self.canvas.zoom.get()/40
        new_x0 = x0 + dx * r / dist
        new_y0 = y0 + dy * r / dist
        new_x1 = x1 - dx * r / dist
        new_y1 = y1 - dy * r / dist

        tx = x0 + (x1 - x0) * (2 / 3)
        ty = y0 + (y1 - y0) * (2 / 3)

        self.canvas_id = self.canvas.draw_line(new_x0, new_y0, new_x1, new_y1)
        self.label_id = self.canvas.create_text(tx, ty, text=f'{self.ids}', fill="black", font=("Arial", 10))

    def add_paralel(self, edge_id):
        self.ids.append(edge_id)
