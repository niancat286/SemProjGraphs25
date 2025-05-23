import math
import tkinter as tk

class LineSegment:
    def __init__(self, x0, y0, z0, x1, y1, z1, canvas, edge_id, color = 'blue', width=1, arrow = None):
        self.P0 = [x0, y0, z0]
        self.P1 = [x1, y1, z1]
        self.compare_z = max(z0, z1)
        self.color = color
        self.width=width
        self.canvas = canvas
        self.canvas_id = None
        self.label_id = None
        self.arrow = arrow
        self.ids = [*edge_id]

    def erase(self):
        if(self.canvas_id is not None):
            self.canvas.delete(self.canvas_id)
        if self.label_id is not None:
            self.canvas.delete(self.label_id)


    def draw(self):
        self.erase()

        try:
            x0, y0 = self.canvas.project_point(*self.P0)
            x1, y1 = self.canvas.project_point(*self.P1)
            self.canvas_id = self.canvas.create_line(x0, y0, x1, y1, fill=self.color, width=self.width, arrow=self.arrow)
        except IndexError:
            pass


class Edge:
    def __init__(self, vertex1, vertex2, edge_id, canvas):
        self.__v1 = vertex1
        self.__v2 = vertex2
        self.ids = [*edge_id]

        self.canvas = canvas
        self.canvas_id = None  # id лінії
        self.label_id = None  # id тексту

    def calc_segments(self):
        V1, V2, arrow = self.calc_begin_end()
        if V1 is None:
            return []
        canvas = self.canvas

        if V1 == V2:
            x0, y0, z0 = V1
            r_vertex = self.__v1.r
            r_loop = r_vertex * 1.8  # трохи більша дуга

            # Зміщення центру дуги: праворуч від вершини
            offset_x = x0 + r_loop
            offset_y = y0
            offset_z = z0

            # Кутова амплітуда дуги
            angle_start = math.radians(210)
            angle_end = math.radians(-150)
            num_segments = 12

            segments = []
            for i in range(num_segments):
                t1 = angle_start + (angle_end - angle_start) * i / num_segments
                t2 = angle_start + (angle_end - angle_start) * (i + 1) / num_segments

                # Точки дуги в XY площині (можна адаптувати до іншої)
                x1 = offset_x + r_loop * math.cos(t1)
                y1 = offset_y + r_loop * math.sin(t1)
                z1 = offset_z + 0.01  # трохи вище — щоб не зливалося

                x2 = offset_x + r_loop * math.cos(t2)
                y2 = offset_y + r_loop * math.sin(t2)
                z2 = offset_z + 0.01

                segment = LineSegment(
                    x0=x1, y0=y1, z0=z1,
                    x1=x2, y1=y2, z1=z2,
                    canvas=self.canvas,
                    edge_id=self.ids
                )
                segments.append(segment)

            if segments:
                segments[-1].arrow = 'last'

            return segments

        x1, y1, z1 = V1
        x2, y2, z2 = V2
        L = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
        N = int(L)+1
        
        segments = []
    
        # Generate N equal-length segments
        for i in range(N):
            # Parameter t for start and end of segment
            t_start = i / N
            t_end = (i + 1) / N
        
            # Calculate start point of segment
            x0 = x1 + t_start * (x2 - x1)
            y0 = y1 + t_start * (y2 - y1)
            z0 = z1 + t_start * (z2 - z1)
        
            # Calculate end point of segment
            x1_seg = x1 + t_end * (x2 - x1)
            y1_seg = y1 + t_end * (y2 - y1)
            z1_seg = z1 + t_end * (z2 - z1)
        
            # Create LineSegment object
            segment = LineSegment(x0=x0, y0=y0, z0=z0, x1=x1_seg, y1=y1_seg, z1=z1_seg, canvas=canvas, edge_id=self.ids)

            segments.append(segment)

        last = segments[-1]
        last.compare_z = min(last.P0[2], last.P1[2]) 
        last.arrow = arrow
        return segments

    def calc_begin_end(self):
        # Отримуємо координати вершин
        x0, y0, z0 = self.__v1.x, self.__v1.y, self.__v1.z
        x1, y1, z1 = self.__v2.x, self.__v2.y, self.__v2.z

        r = self.__v1.r


        # Перевірка на петлю (ребро з вершини в саму себе)
        if self.__v1 == self.__v2:
            # Повертаємо одні й ті самі координати — обробка буде в calc_segments
            return [x0, y0, z0], [x1, y1, z1], None

        # Вектор між вершинами
        u = [x1 - x0, y1 - y0, z1 - z0]
        dist = (u[0] ** 2 + u[1] ** 2 + u[2] ** 2) ** 0.5

        # Якщо вершини занадто близько — не малюємо ребро
        if dist < r * 2:
            drawn = 1
            self.canvas_id = None
            self.label_id = None
            return None, None, None

        # Нормалізуємо напрям
        u = [u[0] / dist, u[1] / dist, u[2] / dist]
        eps = 0.0001

        # Зсуваємо на радіус, щоб не малювати до центру вершини
        A = [x0 + (r * u[0]) - eps, y0 + (r * u[1]) - eps, z0 + (r * u[2]) - eps]
        B = [x1 - (r * u[0]), y1 - (r * u[1]), z1 - (r * u[2])]

        # Кліпінг за z
        if A[2] < self.canvas.clipping_z and B[2] < self.canvas.clipping_z:
            return None, None, None

        arrow = 'last'
        _V1 = A
        _V2 = B

        # Частковий кліпінг
        if B[2] < self.canvas.clipping_z or A[2] < self.canvas.clipping_z:
            t = (self.canvas.clipping_z - A[2]) / (B[2] - A[2])
            x = A[0] + t * (B[0] - A[0])
            y = A[1] + t * (B[1] - A[1])
            if B[2] < self.canvas.clipping_z:
                _V1 = A
                _V2 = [x, y, self.canvas.clipping_z + 0.01]
                arrow = None
            else:
                _V1 = [x, y, self.canvas.clipping_z + 0.01]
                _V2 = B

        return _V1, _V2, arrow

    def draw(self):
        if self.canvas_id is not None:
            self.canvas.delete(self.canvas_id)
            #self.canvas.delete(self.label_id)
        _V1, _V2, arrow = self.calc_begin_end()
        x0, y0 = self.canvas.project_point(*_V1)
        x1, y1 = self.canvas.project_point(*_V2)

        if _V1 == _V2:
            print(x0, y0)
            print(x1, y1)

        if(x0 == None):
            print('THIS WAS NOT SUPPOSSED TO HAPPEN')
            raise Exception
        self.canvas_id = self.canvas.create_line(x0, y0, x1, y1, fill='blue', arrow = arrow)



    def add_paralel(self, edge_id):
        self.ids.append(edge_id)


class Label_name:
    def __init__(self, vertex1, vertex2, canvas, edge_id):
        self.__v1 = vertex1
        self.__v2 = vertex2
        self.canvas = canvas
        self.label_id = None
        self.ids = [*edge_id]  # список ID

    def erase(self):
        if self.label_id is not None:
            self.canvas.delete(self.label_id)
            self.label_id = None

    def draw(self):
        # Отримуємо координати з урахуванням трансформації
        x0, y0, z0 = self.__v1.x, self.__v1.y, self.__v2.z
        x1, y1, z1 = self.__v2.x, self.__v2.y, self.__v2.z

        # Обчислюємо позицію тексту трохи ближче до __v2
        try:
            if self.__v1.number == self.__v2.number:
                # Це петля
                # радіус петлі (такий самий, як при малюванні)
                r_loop = self.__v1.r * 1.9  # трохи більша дуга

                # Зміщення центру дуги: праворуч від вершини
                offset_x = x0 + r_loop
                offset_y = y0
                offset_z = z0

                # Кутова амплітуда дуги
                angle_start = math.radians(210)
                angle_end = math.radians(0)
                num_segments = 12

                for i in range(num_segments):
                    t2 = angle_start + (angle_end - angle_start) * (i + 1) / num_segments

                    # Точки дуги в XY площині (можна адаптувати до іншої)

                    x2 = offset_x + r_loop * math.cos(t2)
                    y2 = offset_y + r_loop * math.sin(t2)
                    z2 = offset_z

                tx, ty = self.canvas.project_point(x2, y2, z2)

            else:
                # Стандартне ребро
                # Вектор від v1 до v2
                x0_2d, y0_2d = self.canvas.project_point(x0, y0, z0)
                x1_2d, y1_2d = self.canvas.project_point(x1, y1, z1)

                dx = x1_2d - x0_2d
                dy = y1_2d - y0_2d

                # Точка ближче до v2 (2:3)
                tx = x0_2d + dx * 0.6
                ty = y0_2d + dy * 0.6


            if self.ids:
                label_text = ','.join(str(i) for i in self.ids)
                self.label_id = self.canvas.create_text(
                    tx, ty,
                    text=f'[{label_text}]',
                    fill="red",
                    font=("Arial", 10)
                )
        except TypeError:
            pass
        except IndexError:
            pass
