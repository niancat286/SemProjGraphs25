from collections import defaultdict


class Graph:
    def __init__(self, filename=None):
        self.N = 0
        self._matrix_adjacency = []

        if filename is not None:
            matrix, success = self.read_matrix_with_limits(filename)
            if success:
                self._matrix_adjacency = self.read(matrix)
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

    def __str__(self):
        line = ''
        vertices = sorted(set(i for i in self._matrix_adjacency) | {v for d in self._matrix_adjacency.values() for v in d})
        for i in vertices:
            row = []
            for j in vertices:
                row.append(self._matrix_adjacency[i].get(j, []))
            line += f"{i}: {row} \n"
        return line



    def give_vertex(self, v):
            pass


if __name__ == '__main__':
    filename = "matrix.txt"
    M = Graph(filename)
    print(M)