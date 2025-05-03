from tkinter import *
from tkinter import filedialog
from threading import Thread, Event
from time import sleep

MAX_ELEMS = 50
r = 25


def init():
    global numOfTop, active_vertex, cord, graph, selected_vertex, selected_vertex_for_delete, visited, finished, b, e, que, answer
    numOfTop = 0
    selected_vertex = None
    selected_vertex_for_delete = None
    active_vertex = [False] * MAX_ELEMS
    cord = [(0, 0, 0)] * MAX_ELEMS  # третя координата це імʼя вершини

    graph = []
    for c in range(MAX_ELEMS):
        graph.append([0] * MAX_ELEMS)

    visited = []
    finished = []

    b = 0
    e = 0
    que = [0] * MAX_ELEMS

    answer = 'Hello!'


if __name__ == '__main__':
    init()

    root = Tk()
    canvas = Canvas(root, width=800, height=800)
    canvas.pack(side=LEFT)

    button_exp_file = Button(canvas, text='Load graph', command=print('exp_file'))
    button_exp_file.place(x=10, y=10)

    button_find_file = Button(canvas, text='Find way', command=print('find_file'))
    button_find_file.place(x=10, y=40)

    button_save_file = Button(canvas, text='Save graph', command=print('Save graph'))
    button_save_file.place(x=115, y=10)

    button_close_file = Button(canvas, text='Exit', command=print('Exit'))
    button_close_file.place(x=725, y=10)

    button_search_file = Button(canvas, text='DFS', command=print('DFS'))
    button_search_file.place(x=250, y=10)

    button_search_file = Button(canvas, text='BFS', command=print('BFS'))
    button_search_file.place(x=325, y=10)

    answer_Lab = Label(root, text='Hello..')
    answer_Lab.place(x=425, y=10)

    root.mainloop()

"""    canvas.bind('<Button-1>', onCanvasClickLeft)
    canvas.bind('<Button-2>', onCanvasClickRight)
    canvas.bind('<Control-Button-1>', selectStart, "+")
    canvas.bind('<Shift-Control-Button-1>', selectEnd, "+")"""

