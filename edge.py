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
        x0,y0 = self.__v1.screen_x, self.__v1.screen_y
        x1,y1 = self.__v2.screen_x, self.__v2.screen_y
        self.canvas_id = self.canvas.draw_line(x0,y0,x1,y1)

    def add_paralel(self, edge_id):
        self.ids.append(edge_id)
