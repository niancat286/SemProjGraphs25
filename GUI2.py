import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from graph import Graph
from canvas import Canvas
import sv_ttk
import math

PI = 3.1415926535

class VertexMover(tk.Toplevel):
    def __init__(self, root, graph, N=15):
        super().__init__(root)
        
        self.title("Move Vertex")
        self.geometry("400x150")
        self.geometry("-50+50")

        self.graph = graph
        self.N = self.graph.N
        self.vertex = None
        
        self.__create_widgets()

    def __create_widgets(self):
        self.__create_chooser()
        self.__create_movers()
        self.__create_close_button()


    def __create_chooser(self):
        frame = ttk.Frame(self)
        frame.pack(side='top', fill = 'x',pady=2,padx=5)
        self.__entry_value = tk.StringVar(value="Input vertex")
        v_vcmd = (self.register(self.on_validate_vertex), '%P')
        entry = ttk.Entry(frame, textvariable = self.__entry_value, validate="all", validatecommand=v_vcmd)
        entry.pack(side='left',fill='x',padx=5)
        entry.bind("<FocusIn>", self.on_focus_in)
        entry.bind("<FocusOut>", self.on_focus_out)
        ttk.Button(frame, text="Choose", command=self.select_vertex).pack(side='right', padx=5)
   
    def __create_movers(self):
        frame = ttk.Frame(self)
        frame.pack(pady=5,padx=5, fill='x')
        self.__x_spinbox, self.__x_var = self.__create_spinbox(frame,0,'X:', self.move_vertex)
        frame.grid_columnconfigure(1, weight=1)  
        self.__y_spinbox, self.__y_var  = self.__create_spinbox(frame,2,'Y:', self.move_vertex)
        frame.grid_columnconfigure(3, weight=1) 
        self.__z_spinbox, self.__z_var  = self.__create_spinbox(frame,4,'Z:', self.move_vertex)
        frame.grid_columnconfigure(5, weight=1)


    def __create_spinbox(self, frame,column, text, command):
        ttk.Label(frame, text=text).grid(row=0,column=column, padx=2)
        c_vcmd = (self.register(self.on_validate_coord), '%P')
        var = tk.StringVar(value='')
        spinbox = ttk.Spinbox(frame, textvariable=var, from_ = -100*self.N, to = 100*self.N, state="disabled", command=command, validate='all', validatecommand=c_vcmd)
        spinbox.grid(row=0, column=column+1,padx=2)
        spinbox.bind('<Enter>', command)
        return spinbox, var
        
       # c_vcmd = self._root.register(self.on_validate_coord, '%P')
    
    def __create_close_button(self):
        ttk.Button(self, text='Close window', command=self.destroy).pack(side='top', expand=True)

    def move_vertex(self, *args):
        x,y,z = self.__x_spinbox.get(), self.__y_spinbox.get(), self.__z_spinbox.get()
        if x == '' or y == '' or z == '':
            return
        else:
            self.vertex.move_to(float(x), float(y), float(z))
            self.graph.draw()


    def on_validate_vertex(self, s):
        try:
            #print(s)
            digit = int(s)
            return 0 < digit <= self.N
        except ValueError:
            return s == ""

    def on_validate_coord(self, c):
        try:
            float(c)
            return True
        except ValueError:
            return c == "" or c == '-'

    def on_focus_in(self, *args):
        if not self.__entry_value.get().isdigit():
            self.__entry_value.set("")

    def on_focus_out(self, *args):
        if self.__entry_value.get() == '':
            self.__entry_value.set("Input vertex")

    def select_vertex(self):
        s = self.__entry_value.get()
        if s.isdigit():
            v = int(s)
            self.vertex = self.graph.give_vertex(v)
            state = "normal"      
        else:
            self.vertex = None
            state = "disabled"
        self.set_state(state)

    def set_state(self, state):
        self.__x_spinbox.config(state=state)
        self.__y_spinbox.config(state=state)
        self.__z_spinbox.config(state=state)
        self.set_values(zero= (state=='disabled'))

    def update_values(self):
        if self.vertex is None:
            self.set_values(zero=1)
        else:
            self.set_values()

    def set_values(self, zero=False):
        self.__x_var.set(0 if zero else self.vertex.x)
        self.__y_var.set(0 if zero else self.vertex.y)
        self.__z_var.set(0 if zero else self.vertex.z)


class RotationInterface(ttk.Frame):
    def __init__(self, root, canvas, graph):
        super().__init__(root)
        self.pack(pady=5, fill='x', padx=5)
        self.canvas = canvas
        self.graph = graph
        self.old_x = 0
        self.old_y = 0
        self.old_z = 0
        self.x_angle = tk.DoubleVar(value=0)
        self.y_angle = tk.DoubleVar(value=0)
        self.z_angle = tk.DoubleVar(value=0)
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Label(self, text="Rotation").pack()
        ttk.Button(self, text="Recalculate Centroid", command=self.recalc_centroid).pack(pady=5)
        self.__create_type_chooser()
        self.__create_sliders()
        self.__create_buttons()

    def recalc_centroid(self, *args):
        if not self.switch_var.get():
            self.fix_rotation()
        self.graph.calc_centroid()

    def __create_type_chooser(self):
        frame = ttk.Frame(self)
        frame.pack(pady=2, fill='x')
        ttk.Label(frame, text="Centroid").grid(row=0, column=0, sticky='w', padx=2)

        # Switch in the middle
        self.switch_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, style='Switch.TCheckbutton', variable=self.switch_var, command=self.switch).grid(row=0, column=1, padx=2)
        # https://github.com/rdbende/Sun-Valley-ttk-theme need toggle

        # Spinbox on the right
        ttk.Label(frame, text="V:").grid(row=0, column=2, sticky='e', padx=2)
        self.spinbox_var = tk.StringVar(value="1")
        vspn = (self.register(self.on_validate_vertex), "%P")
        spinbox = ttk.Spinbox(
            frame,
            from_=1,
            to=self.graph.N,
            textvariable=self.spinbox_var,
            validate="key",
            validatecommand=vspn
        )
        spinbox.grid(row=0, column=3, sticky='e', padx=2)
        spinbox.bind("<Return>", lambda event: self.update_spinbox())
        spinbox.bind("<FocusOut>", lambda event: self.update_spinbox())

        # Configure column weights
        frame.columnconfigure(3, weight=1)

    def switch(self):
        self.fix_rotation()

    def update_spinbox(self):
        try:
            value = int(self.spinbox_var.get())
            if 1 <= value <= self.graph.N:
                self.vertex = (value)
        except ValueError:
            self.spinbox_var.set("1")

    def on_validate_vertex(self, value):
        if value == "":
            return True
        try:
            v = int(value)
            return 1 <= v <= self.graph.N
        except ValueError:
            return False

    def __create_sliders(self):
        #ttk.Frame()
        self.__create_slider('X:', self.x_angle)
        self.__create_slider('Y:', self.y_angle)
        self.__create_slider('Z:', self.z_angle)

    def __create_slider(self,text, variable):
        slider_frame = ttk.Frame(self)
        slider_frame.pack(pady=2,fill='x')
        ttk.Label(slider_frame, text=text).grid(row=0, column=0, sticky='w',padx=2)
        ttk.Scale(slider_frame, variable=variable, from_=-PI, to=PI, command=self.rotate).grid(row=0, column=1, sticky='ew', padx=2)
        slider_frame.columnconfigure(1, weight=1)
        return

    def rotate(self, *args):
        x, y, z = self.x_angle.get(), self.y_angle.get(), self.z_angle.get()
        if not (x == y == z == 0):
            if self.switch_var.get():
                self.graph.rotate_around_vertex(int(self.spinbox_var.get()), self.old_x, self.old_y, self.old_z,
                                                revert=1)
            else:
                self.graph.rotate_around_centroid(self.old_x, self.old_y, self.old_z, revert=1)
        if self.switch_var.get():
            self.graph.rotate_around_vertex(int(self.spinbox_var.get()), x, y, z)
        else:
            self.graph.rotate_around_centroid(x, y, z)
        self.old_x = x
        self.old_y = y
        self.old_z = z

    def __create_buttons(self):
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=1, fill='x')

        ttk.Button(btn_frame, text="Reset", command=self.reset_rotation).pack(side='right',expand=True)
        ttk.Button(btn_frame, text="Fix", command=self.fix_rotation).pack(side='right',expand=True)

    def fix_rotation(self, *args):
        self.set_to(0)

    def reset_rotation(self, *args):
        if self.switch_var.get():
            self.graph.rotate_around_vertex(int(self.spinbox_var.get()), self.old_x, self.old_y, self.old_z, revert=1)
        else:
            self.graph.rotate_around_centroid(self.old_x, self.old_y, self.old_z, revert=1)
        self.set_to(0)

    def set_to(self, val):
        self.x_angle.set(val)
        self.y_angle.set(val)
        self.z_angle.set(val)
        self.old_x = val
        self.old_y = val
        self.old_z = val


class DragInterface(ttk.Frame):
    def __init__(self, root, canvas, graph):
        super().__init__(root)
        self.graph = graph
        self.pack(pady=5, fill='x', padx=5)
        self.canvas = canvas
        self.__create_drag_buttons()

    def __create_drag_buttons(self):
        ttk.Button(self, text="⬆", command=self.move_up).grid(row=0, column=1, pady=5)
        ttk.Button(self, text="⬅", command=self.move_left).grid(row=1, column=0, pady=5)
        ttk.Button(self, text="⮕", command=self.move_right).grid(row=1, column=2, pady=5)
        ttk.Button(self, text="⬇", command=self.move_down).grid(row=2, column=1, pady=5)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    def move_up(self, step=5):
        self.graph.move_for(0, step)

    def move_down(self, step=5):
        self.graph.move_for(0, -step)

    def move_right(self, step=5):
        self.graph.move_for(step, 0)

    def move_left(self, step=5):
        self.graph.move_for(-step, 0)


class Controls(ttk.Frame):
    def __init__(self, root, canvas, graph, relx=0.81, rely=0.01, relwidth=0.19, relheight=0.98, anchor="nw"):
        super().__init__(root)
        self.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight, anchor=anchor)

        self.canvas = canvas
        self.graph = graph
        self.vertex_mover = None
        self.__create_widgets()

    def update_vm(self):
        if self.vertex_mover is None:
            return
        else:
            self.vertex_mover.update_values()

    def __create_widgets(self):
        self.__create_vertex_mover_button()
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(side='top', fill='x')
        self.__create_zoom_slider()
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(side='top', fill='x')
        self.__create_rotation_interface()
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(side='top', fill='x')
        self.__create_drag_interface()
        self.__create_labels_controls()

    def __create_labels_controls(self):
        ttk.Checkbutton(self, text='Edge labels', variable=self.graph.label_state, command=lambda *args:self.graph.draw()).pack(side='bottom', pady = 2)

    def __create_vertex_mover_button(self):
        ttk.Button(self, text='Move vertex', command=self.create_vertex_mover, state='normal').pack(side='top', pady=2)

        #self._vertex_mover_button.place(relx=0.01, rely=0.09, relwidth=0.15, relheight=0.06, anchor='ne')

    def create_vertex_mover(self):
        if self.vertex_mover is None:
            self.vertex_mover = VertexMover(self, self.graph)
            self.vertex_mover.bind("<Destroy>", self.on_vertex_mover_destroy)
        else:
            self.vertex_mover.lift()

    def on_vertex_mover_destroy(self, event):
        self.vertex_mover = None


    def __create_zoom_slider(self):
        frame = ttk.Frame(self)
        frame.pack(padx=3, pady=3, fill='x')
        ttk.Label(frame, text="Zoom").pack(side='top', pady=(5, 3))
        self.zoom = tk.DoubleVar(value=0)
        self.prev_zoom = 0
        ttk.Scale(
            frame,
            variable=self.zoom,
            from_=1000.0,
            to=-1000,
            orient="horizontal",
            command=self.on_zoom
        ).pack(pady=3, padx=5, fill='x')
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=3, fill='x')
        ttk.Button(btn_frame, text='Center slider', command=self.center_zoom).pack(side='top')

    def center_zoom(self):
        self.zoom.set(0)
        self.prev_zoom = 0

    def on_zoom(self, e):
        self.graph.zoom_for(self.zoom.get() - self.prev_zoom)
        self.prev_zoom = self.zoom.get()

    def __create_rotation_interface(self):
        self.__rotation_interface = RotationInterface(self, self.canvas, self.graph)

    def __create_drag_interface(self):
        self.__drag_interface = DragInterface(self, self.canvas, self.graph)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        sv_ttk.set_theme("dark")
        self.__create_widgets()
        self.mainloop()

    
    def __implement_mouse_zooming(self):
        root = self
        root.bind("<MouseWheel>", self.mouse_wheel)
        # with Linux OS
        root.bind("<Button-4>", self.mouse_wheel)
        root.bind("<Button-5>", self.mouse_wheel)
        
    def mouse_wheel(self, event):
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            self.zoom.set(self.zoom.get() - 1) 
            print('down')
        if event.num == 4 or event.delta == 120:
            self.zoom.set(self.zoom.get() + 1)
            print('up')
        self.graph.draw()



    def __create_widgets(self):
        self.__create_canvas()
        self.__create_import_button()
        
    def __create_controls(self):
        self.controls = Controls(self, rely=0.06,relheight=0.92, canvas=self.canvas, graph=self.graph)

    def __create_canvas(self):
        self.canvas = Canvas(self)
       
    def __create_import_button(self):
        ttk.Button(self, text='Import graph', command=self.import_graph).place(relx=0.905, rely=0.004, relwidth=0.1, relheight=0.05, anchor='n')


    def import_graph(self):
        filename = tk.filedialog.askopenfilename(defaultextension = ".txt",
                                                 filetypes = (("Text Files", "*.txt"),
                                                              ("All Files", "*.*")))
     #   self.__graph = Graph(filename)
     #   self.__create_controls()
     #   self.__canvas.redraw()

        self.graph = Graph(self.canvas, filename)

        try:
            self.graph = Graph(self.canvas, filename)
        except Exception as e:
            print(e)
            tk.messagebox.showerror(title=None, message="Некоректні дані")
            return
        self.canvas.graph = self.graph
        self.canvas.implement_controls()
        self.graph.draw()
        self.__create_controls()
        self.graph.controls = self.controls
        self.__implement_mouse_zooming()
        


       # try:
       #     self.__graph = Graph(self.__canvas, filename)
       #     self.__graph.draw()
       #     self.__create_controls()
       #     self.__canvas.redraw()
       # except Exception as e:
       #     print(e)
       #     tk.messagebox.showerror(title=None, message="Некоректні дані")
       #     #return
       #     # the next line is for debugging purposes
       #     self.__graph = Graph(self.__canvas)

       # self.__create_controls()
       # self.__canvas.redraw()


      #  if(self.__graph.read(filename)):
      #      self.__create_controls()
      #      self.__canvas.redraw()
      #  else:
      #      tk.messagebox.showerror(title=None, message="Некоректні дані")


if __name__ == "__main__":
    g = GUI()


