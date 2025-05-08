from collections import defaultdict
from geometry import generate_points
from vertex import Vertex
from edge import Edge
class Graph:
    def __init__(self, canvas, filename = None):
        self.canvas = canvas
        self.N = 0
        if filename is not None:
            matrix = self.read_matrix_with_limits(filename)
            self._matrix_adjacency = self.read(matrix)
        else:
            self._matrix_adjacency = []


    def read_matrix_with_limits(self, filename, max_rows=15, max_cols=7):
        matrix = []
        with open(filename, 'r') as file:
            for line in file:
                if len(matrix) >= max_rows:
                    break
                row = list(map(int, line.strip().split()))
                matrix.append(row[:max_cols])
        return matrix

    def read(self, matrix):
        adj = defaultdict(lambda: defaultdict(list))  # adj[src][dst] = [edge_numbers]

        for i, row in enumerate(matrix):  # i — джерело, вершина i+1
            src = i + 1
            for j, dst in enumerate(row):  # j — номер ребра (з 0), dst — вершина призначення
                adj[src][dst].append(j)
        self.N = len(matrix)
        self.create_elements(adj)
        return adj

    def create_elements(self, adj):
        self.vertices = [-1,]
        self.edges = []
        coords = generate_points(self.N)
        print(coords)
        for i in range(self.N):
            self.vertices.append(Vertex(*coords[i], number = i+1, canvas = self.canvas))
        j=-1
        for src in adj:
            for dst in adj[src]:
                self.edges.append(Edge(self.vertices[src], self.vertices[dst], edge_id = adj[src][dst], canvas = self.canvas))
                j+=1
                self.vertices[src].out_edges.append(self.edges[j])
                self.vertices[dst].in_edges.append(self.edges[j])
        return

    def draw(self, *args):
        for vertex in self.vertices[1:]:
            vertex.draw()

        for edge in self.edges:
            edge.draw()

            


    def __str__(self):
        line = ''
        vertices = sorted(set(i for i in self._matrix_adjacency) | {v for d in self._matrix_adjacency.values() for v in d})
        for i in vertices:
            row = []
            for j in vertices:
                row.append(self._matrix_adjacency[i].get(j, []))
            line += (f"{i}: {row} \n")

        return line



    def give_vertex(self, v):
        return self.vertices[v]
        pass


if __name__ == '__main__':
    filename = "matrix.txt"
    M = Graph(filename)
    print(M)
