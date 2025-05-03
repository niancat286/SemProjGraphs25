import tkinter as tk
from tkinter import ttk, filedialog
from graph import Graph
from canvas import Canvas

class VertexMover():
    def __init__(self, root, graph, N=15):
        self._root = root
        self._graph = graph
        self._N = N
        self._vertex = None
        self._entry_value = tk.StringVar(value="Input vertex")
        v_vcmd = (self._root.register(self.on_validate_vertex), '%P')
        self._vertex_entry = ttk.Entry(self._root, textvariable = self._entry_value, validate="all", validatecommand=v_vcmd)
        self._vertex_entry.place(relx=0.91, rely=0.11, relwidth=0.09, relheight=0.07, anchor='ne')
        self._vertex_entry.bind("<FocusIn>", self.on_focus_in)
        self._vertex_entry.bind("<FocusOut>", self.on_focus_out)
        self._choose_button = ttk.Button(self._root, text="Choose")
        self._choose_button.place(relx=0.99, rely=0.11, relwidth=0.07, relheight=0.07, anchor='ne')

        c_vcmd = self._root.register(self.on_validate_coord, '%P')

        self._x_label = ttk.Label(self._root, text="X:")
        self._x_value = tk.StringVar(value = 0)
        self._x_spinbox = ttk.Spinbox(self._root, textvariable=self._x_value, from_ = -100*self._N, to = 100*self._N, state="disabled", command=self.move_x)
    
        self._x_label.place(relx = 0.89, rely = 0.21, relwidth = 0.03, relheight=0.07, anchor='ne')
        self._x_spinbox.place(relx = 0.95, rely = 0.21, relwidth = 0.05, relheight = 0.07, anchor='ne')


        self._y_label = ttk.Label(self._root, text="Y:")
        self._y_value = tk.StringVar(value = 0)
        self._y_spinbox = ttk.Spinbox(self._root, textvariable=self._y_value, from_ = -100*self._N, to = 100*self._N, state="disabled", command=self.move_y)
        
        self._y_label.place(relx = 0.89, rely = 0.28, relwidth = 0.03, relheight=0.07, anchor='ne')
        self._y_spinbox.place(relx = 0.95, rely = 0.28, relwidth = 0.05, relheight = 0.07, anchor='ne')

        self._z_label = ttk.Label(self._root, text="Z:")
        self._z_value = tk.StringVar(value = 0)
        self._z_spinbox = ttk.Spinbox(self._root, textvariable=self._z_value, from_ = -100*self._N, to = 100*self._N, state="disabled",command=self.move_z)
        
        self._z_label.place(relx = 0.89, rely = 0.35, relwidth = 0.03, relheight=0.07, anchor='ne')
        self._z_spinbox.place(relx = 0.95, rely = 0.35, relwidth = 0.05, relheight = 0.07, anchor='ne')

        self._choose_button['command'] = self.select_vertex


    def on_validate_vertex(self, s):
        try:
            print(s)
            digit = int(s)
            return 0 < digit <= self._N
        except ValueError:
            return s == ""

    def on_validate_coord(self, c):
        try:
            float(c)
            return True
        except ValueError:
            return False

    def on_focus_in(self, event):
        if not self._entry_value.get().isdigit():
            self._entry_value.set("")

    def on_focus_out(self, event):
        if self._entry_value.get() == '':
            self._entry_value.set("Input vertex")

    def select_vertex(self):
        s = self._entry_value.get()
        if s.isdigit():
            v = int(s)
            self._vertex = self._graph.give_vertex(v)
            state = "Normal"      
            self._x_value.set(self._vertex.x)
            self._y_value.set(self._vertex.y)
            self._z_value.set(self._vertex.z)

        else:
            self._vertex = None
            state = "Disabled"
        self._x_spinbox.config(state=state)
        self._y_spinbox.config(state=state)
        self._z_spinbox.config(state=state)

    def move_x(self):
        x = float(self._x_value.get())
        self._vertex.move_x(x)
    
    def move_y(self):
        y = float(self._y_value.get())
        self._vertex.move_y(y)

    def move_z(self):
        z = float(self._z_value.get())
        self._vertex.move_z(z)








class GUI():
    def __init__(self):
        self._root = tk.Tk()
        self._root.geometry("1280x720")
        self._graph = Graph()

        self._create_widgets()
        self._root.mainloop()


    def _create_widgets(self):
        self._create_canvas()
        self._create_import_button()
        self._create_vertex_mover()
        self._create_zoom_slider()
        self._create_rotation_interface()

    def _create_canvas(self):
        self._canvas = Canvas(self._root)

    def _create_import_button(self):
        self._import_graph_button = ttk.Button(self._root, text='Import graph', command=self._import_graph)
        self._import_graph_button.place(relx=0.99, rely=0.01, relwidth=0.15, relheight=0.085, anchor='ne')
    
    def _create_vertex_mover(self):
        self._vertex_mover = VertexMover(self._root, self._graph)

    def _create_zoom_slider(self):
        pass

    def _create_rotation_interface(self):
        pass

    def _import_graph(self):
        filename = tk.filedialog.askopenfilename(defaultextension = ".txt",
                                                 filetypes = (("Text Files", "*.txt"),
                                                              ("All Files", "*.*")))
        self._graph = Graph(filename)

        if(self._graph.read(filename)):
            self._canvas_update()
            self.vertex_mover = VertexMover(self._root, self._graph)


    def _canvas_update(self):
        self._canvas.update()


if __name__ == "__main__":
    g = GUI()

