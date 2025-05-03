class Edge:
    def __init__(self, vertex1, vertex2, edge_id):
        self._v1 = vertex1
        self._v2 = vertex2
        self.ids = [edge_id]

        self.canvas_id = None  # id лінії
        self.label_id = None  # id тексту


def add_paralel(self, edge_id):
        self.ids.append(edge_id)
