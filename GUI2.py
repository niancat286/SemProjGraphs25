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






class GUI():
    def __init__(self):
        self._root = tk.Tk()
        self._root.geometry("1280x720")
        sv_ttk.set_theme("dark")

        self._create_widgets()
                
        self._graph = Graph()
        self._vertex_mover = None 

        self._root.mainloop()

    def _create_widgets(self):
        self._create_canvas()
        self._create_import_button()
        self._create_vertex_mover_button()
        self._create_zoom_slider()
        self._create_rotation_interface()

    def _create_vertex_mover_button(self):
        self._vertex_mover_button = ttk.Button(self._root, text='Move vertex', command=self._create_vertex_mover, state='disabled')
        self._vertex_mover_button.place(relx=0.98, rely=0.09, relwidth=0.15, relheight=0.06, anchor='ne')

    def _create_vertex_mover(self):
        if self._vertex_mover is None:
            self._vertex_mover = VertexMover(self._root, self._graph)
        else:
            self._vertex_mover.show()


    def _create_canvas(self):
        self._canvas = Canvas(self._root)
       
    def _create_import_button(self):
        self._import_graph_button = ttk.Button(self._root, text='Import graph', command=self._import_graph)
        self._import_graph_button.place(relx=0.98, rely=0.02, relwidth=0.15, relheight=0.06, anchor='ne')
       
    def _create_zoom_slider(self):
        self._zoom_label = ttk.Label(self._root, text="Zoom")
        self._zoom_label.place(relx=0.98, rely=0.16, relwidth=0.1, relheight=0.035, anchor="ne")
        self._zoom_slider = ttk.Scale(self._root, from_=400.0, to=0.1, orient="horizontal", command=self._update_zoom)
        self._zoom_slider.set(self._canvas.zoom)
        self._zoom_slider.place(relx=0.98, rely=0.197, relwidth=0.15, relheight=0.04, anchor="ne")

    def _update_zoom(self, *args):
        self._canvas.zoom = self._zoom_slider.get()
        self._canvas.redraw()

    def _create_rotation_interface(self):
        self.__rot_label = ttk.Label(self._root, text="Rotation",justify="center")
        self.__rot_label.place(relx=0.915, rely=0.25, relwidth=0.1, relheight=0.035,anchor="center")

        self.__create_x_rot_slider()
        self.__create_y_rot_slider()
        self.__create_z_rot_slider()
        self.__create_reset_rot_button()
        self.__create_fix_rot_button()


    def __create_x_rot_slider(self):
        self.__x_rot_label = ttk.Label(self._root, text="X:")
        self.__x_rot_label.place(relx=0.811, rely=0.285, relwidth=0.015, relheight=0.04, anchor="nw")

        self.x_rotation_slider = ttk.Scale(self._root, from_=-PI, to=PI, orient="horizontal", command=self._canvas.redraw())
        self.x_rotation_slider.set(0)
        self.x_rotation_slider.place(relx=0.98, rely=0.285,  relwidth=0.15, relheight=0.04, anchor="ne")

    def __create_y_rot_slider(self):
        self.__y_rot_label = ttk.Label(self._root, text="Y:")
        self.__y_rot_label.place(relx=0.811, rely=0.325, relwidth=0.015, relheight=0.04, anchor="nw")

        self.y_rotation_slider = ttk.Scale(self._root, from_=-PI, to=PI, orient="horizontal", command=self._canvas.redraw())
        self.y_rotation_slider.set(0)
        self.y_rotation_slider.place(relx=0.98, rely=0.325, relwidth=0.15, relheight=0.04, anchor="ne")

    def __create_z_rot_slider(self):
        self.__z_rot_label = ttk.Label(self._root, text="Z:")
        self.__z_rot_label.place(relx=0.811, rely=0.365, relwidth=0.015, relheight=0.04, anchor="nw")

        self.z_rotation_slider = ttk.Scale(self._root, from_=-PI, to=PI, orient="horizontal", command=self._canvas.redraw())
        self.z_rotation_slider.set(0)
        self.z_rotation_slider.place(relx=0.98, rely=0.365, relwidth=0.15, relheight=0.04, anchor="ne")

    def __create_reset_rot_button(self):
        ttk.Button(self._root, text="Reset", command=self.__reset_rotation).place(relx=0.98, rely=0.405, relwidth=0.075, relheight=0.05, anchor="ne")

    def __create_fix_rot_button(self):
        ttk.Button(self._root, text="Fix", command=self.__fix_rotation).place(relx=0.82, rely=0.405, relwidth=0.075, relheight=0.05,  anchor="nw")

    def __reset_rotation(self):
        pass

    def __fix_rotation(self):
        pass

    def _import_graph(self):
        filename = tk.filedialog.askopenfilename(defaultextension = ".txt",
                                                 filetypes = (("Text Files", "*.txt"),
                                                              ("All Files", "*.*")))
#        self._graph = Graph(filename)

     #   if(self._graph.read(filename)):
         #   self._canvas_redraw()
        #    self.vertex_mover = VertexMover(self._root, self._graph)
        self._vertex_mover_button.config(state='normal')


    def _canvas_update(self):
        self._canvas.redraw()


if __name__ == "__main__":
    g = GUI()


