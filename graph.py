from geometry import generate_points
from vertex import Vertex
from edge import Edge
from collections import defaultdict
from edge import Label_name
import numpy as np
import math
import tkinter as tk

class Graph:
    def __init__(self, canvas, filename = None):
        self.canvas = canvas
        self.N = 0
        self.__matrix_adjacency = []
        self.label_state = tk.BooleanVar(value=True)

        self.elements = []
        if filename is not None:
            matrix, success = self.read_matrix_with_limits(filename)
            if success:
                self.__matrix_adjacency = self.read(matrix)
                self.N = len(matrix)
                self.create_elements(self.__matrix_adjacency)
            else:
                print(f"[Помилка] Не вдалося зчитати файл: {filename}")

    def read_matrix_with_limits(self, filename, max_rows=15, max_cols=7):
        matrix = []
        try:
            with open(filename, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    if len(matrix) >= max_rows:
                        break

                    parts = line.strip().split()
                    if not parts:
                        continue

                    if any(not part.isdigit() for part in parts):
                        raise ValueError(f"Нечислове значення в рядку {line_number}: {line.strip()}")

                    row = list(map(int, parts))
                    if any(x < 1 for x in row):
                        raise ValueError(f"Значення менше 1 в рядку {line_number}: {line.strip()}")

                    matrix.append(row[:max_cols])  # не більше 7 елементів

            for i in range(1, len(matrix)):
                if len(matrix[i-1]) != len(matrix[i]):
                    raise ValueError(f"Значень в рядках неоднакова кількість")

            return matrix, True

        except ValueError as e:
            print(f"[Помилка даних] {e}")
            return [], False
        except FileNotFoundError:
            print("[Файл не знайдено]")
            return [], False

    def read(self, matrix):
        adj = defaultdict(lambda: defaultdict(list))

        for i, row in enumerate(matrix):  # вершина i+1
            src = i + 1
            for j, dst in enumerate(row):  # ребро j → dst
                adj[src][dst].append(j)
        return adj

    def create_elements(self, adj):
        self.vertices = []
        self.edges = []
        self.labels = []

        coords = generate_points(self.N)
       # print(coords)
        for i in range(self.N):
            self.vertices.append(Vertex(*coords[i], number = i+1, canvas = self.canvas))
        j=-1
        for src in adj:
            for dst in adj[src]:
                self.edges.append(Edge(self.vertices[src-1], self.vertices[dst-1], edge_id = adj[src][dst], canvas = self.canvas))
                j+=1
                self.vertices[src-1].out_edges.append(self.edges[j])
                self.vertices[dst-1].in_edges.append(self.edges[j])

                label = Label_name(self.vertices[src-1], self.vertices[dst-1], canvas=self.canvas, edge_id=adj[src][dst])
                self.labels.append(label)
        self.calc_centroid()
        return

    def sort_elements(self, elements):
        return sorted(elements, key=lambda element: -element.compare_z)

    def draw(self, *args):
        for element in self.elements:
            element.erase()
        elements = []
        elements += self.vertices
        for vertex in self.vertices:
            vertex.calc_projection()
        for edge in self.edges:
            segments = edge.calc_segments()
            elements += segments

        #self.print_els(elements)

        elements = self.sort_elements(elements)
        #print('after_sort:\n')
        #self.print_els(elements)

        for element in elements:
            element.erase()
            element.draw()

        for label in self.labels:
            label.erase()
        if self.label_state.get():
            for label in self.labels:
                label.draw()

        self.elements = elements
#        print(self.canvas.find_all())

    def rotate_around_vertex(self, v, x_angle, y_angle, z_angle, revert=0):
        V = self.give_vertex(v)
        m = self.calculate_matrix(x_angle, y_angle, z_angle)
        if revert:
            m = np.transpose(m)
        for vertex in self.vertices:
            if vertex == V:
                continue
            vertex.rotate(V.x, V.y, V.z, m)
        self.draw()

    def rotate_around_centroid(self, x_angle, y_angle, z_angle, revert=0, matrix=None):
        if matrix is None:
            m = self.calculate_matrix(x_angle, y_angle, z_angle)
        else:
            m = matrix
        if revert:
            m = np.transpose(m)
        for vertex in self.vertices:
            vertex.rotate(*self.centroid, m)
        self.draw()

    def calculate_matrix(self, x_angle, y_angle, z_angle):

        r_x = [[1, 0, 0],
               [0, math.cos(x_angle), math.sin(x_angle)],
               [0, -math.sin(x_angle), math.cos(x_angle)]]

        r_y = [[math.cos(y_angle), 0, -math.sin(y_angle)],
               [0, 1, 0],
               [math.sin(y_angle), 0, math.cos(y_angle)]]

        r_z = [[math.cos(z_angle), math.sin(z_angle), 0],
               [-math.sin(z_angle), math.cos(z_angle), 0],
               [0, 0, 1]]

        m = np.matmul(np.matmul(r_y, r_x), r_z)
        return m

    def calc_centroid(self):
        centroid = [0, 0, 0]
        for vertex in self.vertices:
            centroid[0] += vertex.x
            centroid[1] += vertex.y
            centroid[2] += vertex.z
        centroid[0] /= self.N
        centroid[1] /= self.N
        centroid[2] /= self.N
        self.centroid = centroid

    def print_els(self, els):
        print('[')
        for el in els:
            print(f'{el.compare_z=}',end=' ')
        print('\n]')

    def __str__(self):
        line = ''
        vertices = sorted(set(i for i in self.__matrix_adjacency) | {v for d in self.__matrix_adjacency.values() for v in d})
        for i in vertices:
            row = []
            for j in vertices:
                row.append(self.__matrix_adjacency[i].get(j, []))
            line += f"{i}: {row} \n"
        return line

    def give_vertex(self, v):
        return self.vertices[v-1]

    def vertex_by_id(self,  ids):
        #print(ids)#according to the documentation last one is the top one 
        vertices = []

        for vertex in self.vertices:
            for i in range(len(ids)):
                if vertex.canvas_id == ids[i] or vertex.label_id == ids[i]:
                    vertices.append(vertex)
        if len(vertices) == 0:
            return None
        else:
            return vertices[-1]

    def move_for(self, x, y, vertex=None):
        vertices = self.vertices if vertex is None else [vertex]
        for vertex in vertices:
            vertex.move_for(x, y)
        self.controls.update_vm()
        self.draw()

    def zoom_for(self, z, vertex=None):
        if vertex is None:
            self.centroid[2] += z
        vertices = self.vertices if vertex is None else [vertex]
        for vertex in vertices:
            vertex.zoom_for(z)
        self.controls.update_vm()
        self.draw()

if __name__ == '__main__':
    filename = "matrix.txt"
    M = Graph(filename)
    print(M)
