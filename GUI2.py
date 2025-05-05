import tkinter as tk
from tkinter import ttk, filedialog
from graph import Graph
from canvas import Canvas
import sv_ttk

PI = 3.1415926535

class VertexMover():
    def __init__(self, root, graph, N=15):
        self._root = tk.Toplevel(root)
        
        self._root.title("Move Vertex")
        self._root.geometry("400x300")
        self._root.geometry("-100-100")
        self._root.protocol("WM_DELETE_WINDOW", self._hide)
        self._root.withdraw()

        self._graph = graph
        self._N = N
        self._vertex = None
        
        self._create_widgets()

    def _create_widgets(self):
        self._create_entry()

        self._create_choose_button()
        self._create_x_spinbox()
        self._create_y_spinbox()
        self._create_z_spinbox()
        self._create_close_button()

    def _create_entry(self):
        self._entry_value = tk.StringVar(value="Input vertex")
        v_vcmd = (self._root.register(self.on_validate_vertex), '%P')
        self._vertex_entry = ttk.Entry(self._root, textvariable = self._entry_value, validate="all", validatecommand=v_vcmd)
        self._vertex_entry.place(relx=0.02, rely=0.02, relwidth=0.45, relheight=0.2, anchor='nw')
        self._vertex_entry.bind("<FocusIn>", self.on_focus_in)
        self._vertex_entry.bind("<FocusOut>", self.on_focus_out)
        
    def _create_choose_button(self):
        self._choose_button = ttk.Button(self._root, text="Choose")
        self._choose_button.place(relx=0.5, rely=0.02, relwidth=0.45, relheight=0.2, anchor='nw')
        self._choose_button['command'] = self.select_vertex

       # c_vcmd = self._root.register(self.on_validate_coord, '%P')
    def _create_x_spinbox(self):
        self._x_label = ttk.Label(self._root, text="X:")
        self._x_value = tk.StringVar(value = 0)
        self._x_spinbox = ttk.Spinbox(self._root, textvariable=self._x_value, from_ = -100*self._N, to = 100*self._N, state="disabled", command=self.move_x)
    
        self._x_label.place(relx = 0.04, rely = 0.3, relwidth = 0.3, relheight=0.1, anchor='nw')
        self._x_spinbox.place(relx = 0.32, rely = 0.3, relwidth = 0.3, relheight = 0.1, anchor='nw')

    def _create_y_spinbox(self):
        self._y_label = ttk.Label(self._root, text="Y:")
        self._y_value = tk.StringVar(value = 0)
        self._y_spinbox = ttk.Spinbox(self._root, textvariable=self._y_value, from_ = -100*self._N, to = 100*self._N, state="disabled", command=self.move_y)
        
        self._y_label.place(relx = 0.04, rely = 0.41, relwidth = 0.3, relheight=0.1, anchor='nw')
        self._y_spinbox.place(relx = 0.32, rely = 0.41, relwidth = 0.3, relheight = 0.1, anchor='nw')
    
    def _create_z_spinbox(self):
        self._z_label = ttk.Label(self._root, text="Z:")
        self._z_value = tk.StringVar(value = 0)
        self._z_spinbox = ttk.Spinbox(self._root, textvariable=self._z_value, from_ = -100*self._N, to = 100*self._N, state="disabled",command=self.move_z)
        
        self._z_label.place(relx = 0.04, rely = 0.52, relwidth = 0.03, relheight=0.1, anchor='nw')
        self._z_spinbox.place(relx = 0.32, rely = 0.52, relwidth = 0.3, relheight = 0.1, anchor='nw')
    
    def _create_close_button(self):
        self._close_button = ttk.Button(self._root, text='Close window', command=self._hide)
        self._close_button.place(relx=0.5, rely = 0.8, relwidth = 0.5, relheight=0.1, anchor='center')





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
            state = "normal"      
            self._x_value.set(self._vertex.x)
            self._y_value.set(self._vertex.y)
            self._z_value.set(self._vertex.z)

        else:
            self._vertex = None
            state = "disabled"
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

    def _hide(self):
        self._root.withdraw()

    def show(self):
        self._root.deiconify()
       # self._root.lift()

    def destroy(self):
        self._root.destroy()


class RotationInterface(ttk.Frame):
    def __init__(self, root, canvas, graph):
        super().__init__(root)
        self.pack(pady=5, fill='x', padx=5)
        self.__canvas = canvas
        self.__graph = graph
        self.__create_widgets()

    def __create_widgets(self):
        self.__label = ttk.Label(self, text="Rotation")
        self.__label.grid(row=0,columnspan=2)
        self.__create_x_rot_slider()
        self.__create_y_rot_slider()
        self.__create_z_rot_slider()
        self.columnconfigure(1, weight=1)
        self.__create_reset_rot_button()
        self.__create_fix_rot_button()


    def __create_x_rot_slider(self):
        ttk.Label(self, text="X:").grid(row=1, column=0, sticky='w')
        self.x_rotation_slider = ttk.Scale(self, from_=-PI, to=PI, command=self.__canvas.redraw())
        self.x_rotation_slider.grid(row=1, column=1, sticky='ew')
        self.x_rotation_slider.set(0)

    def __create_y_rot_slider(self):
        ttk.Label(self, text="Y:").grid(row=2, column=0, sticky='w')
        self.y_rotation_slider = ttk.Scale(self, from_=-PI, to=PI, command=self.__canvas.redraw())
        self.y_rotation_slider.grid(row=2, column=1, sticky='ew')
        self.y_rotation_slider.set(0)

    def __create_z_rot_slider(self):
        ttk.Label(self, text="Z:").grid(row=3, column=0, sticky='w')
        self.z_rotation_slider = ttk.Scale(self, from_=-PI, to=PI, command=self.__canvas.redraw())
        self.z_rotation_slider.grid(row=3, column=1, sticky='ew')

        self.z_rotation_slider.set(0)

    def __create_reset_rot_button(self):
        self.__reset_button = ttk.Button(self, text="Reset", command=self.__reset_rotation)
        self.__reset_button.grid(row=4,column=1)


    def __create_fix_rot_button(self):
        self.__fix_button = ttk.Button(self, text="Fix", command=self.__fix_rotation)
        self.__fix_button.grid(row=4,column=0)

    def __reset_rotation(self):
        pass

    def __fix_rotation(self):
        pass






class Controls(ttk.Frame):
    def __init__(self, root, canvas, graph, relx=0.81, rely=0.01, relwidth=0.19, relheight=0.98, anchor="nw"):
        super().__init__(root)
        self.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight, anchor=anchor)
        self._canvas = canvas
        self.__widgets = []
        self.__graph = graph
        self.__vertex_mover = VertexMover(self, self.__graph)
        self.__create_widgets()

    def __create_widgets(self):
        self._create_vertex_mover_button()
        self._create_zoom_slider()
        self._create_rotation_interface()

    def _create_vertex_mover_button(self):
        self._vertex_mover_button = ttk.Button(self, text='Move vertex', command=self.__vertex_mover.show, state='disabled')
        self._vertex_mover_button.pack(side='top', pady=2)
        #self._vertex_mover_button.place(relx=0.01, rely=0.09, relwidth=0.15, relheight=0.06, anchor='ne')

    def _create_vertex_mover(self):
        if self.__vertex_mover is None:
            self.__vertex_mover = VertexMover(self, self.__graph)
        else:
            self.__vertex_mover.show()

       
    def _create_zoom_slider(self):
        self._zoom_label = ttk.Label(self, text="Zoom")
        self._zoom_label.pack(side='top',pady=(5,3))
        self._zoom_slider = ttk.Scale(self, from_=400.0, to=0.1, orient="horizontal", command=self._update_zoom)
        self._zoom_slider.set(2)#canvas.zoom
        self._zoom_slider.pack(pady=3, padx=5, fill='x')

    def _update_zoom(self, *args):
        self._canvas.zoom = self._zoom_slider.get()
        self._canvas.redraw()

    def _create_rotation_interface(self):
        self.__rotation_interface = RotationInterface(self, self._canvas, self.__graph)
       
    def activate(self):
        for widget in self.__widgets:
            widget.config(state="normal")
            

    def disable(self):
        for widget in self.__widgets:
            widget.config(state="disabled")



class GUI():
    def __init__(self):
        self._root = tk.Tk()
        self._root.geometry("1280x720")
        sv_ttk.set_theme("dark")

        self._graph = Graph()

        self._create_widgets()
        self._root.mainloop()

    def _create_widgets(self):
        self._create_canvas()
        self._create_import_button()
        self._create_controls()
        
    def _create_controls(self):
        self.__controls = Controls(self._root, rely=0.06,relheight=0.92, canvas=self._canvas, graph=self._graph)

    def _create_canvas(self):
        self._canvas = Canvas(self._root)
       
    def _create_import_button(self):
        self._import_graph_button = ttk.Button(self._root, text='Import graph', command=self._import_graph)
        self._import_graph_button.place(relx=0.905, rely=0.0015, relwidth=0.15, relheight=0.05, anchor='n')

    def _import_graph(self):
        filename = tk.filedialog.askopenfilename(defaultextension = ".txt",
                                                 filetypes = (("Text Files", "*.txt"),
                                                              ("All Files", "*.*")))
#        self._graph = Graph(filename)

     #   if(self._graph.read(filename)):
         #   self._canvas_redraw()
        #    self.vertex_mover = VertexMover(self._root, self._graph)
        self.__controls.activate()

    def _canvas_update(self):
        self._canvas.redraw()


if __name__ == "__main__":
    g = GUI()


