from collections import defaultdict

class Graph:
    def __init__(self, filename = None):
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

        return adj

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
            pass


if __name__ == '__main__':
    filename = "matrix.txt"
    M = Graph(filename)
    print(M)