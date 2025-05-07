import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from graph import Graph
from canvas import Canvas
import sv_ttk

PI = 3.1415926535

class VertexMover(tk.Toplevel):
    def __init__(self, root, graph, N=15):
        super().__init__(root)
        
        self.title("Move Vertex")
        self.geometry("400x150")
        self.geometry("-50+50")

        self.__graph = graph
        self.__N = N
        self.__vertex = None
        
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
        self.__x_spinbox = self.__create_spinbox(frame,0,'X:', self.move_vertex)
        frame.grid_columnconfigure(1, weight=1)  
        self.__y_spinbox = self.__create_spinbox(frame,2,'Y:', self.move_vertex)
        frame.grid_columnconfigure(3, weight=1) 
        self.__z_spinbox = self.__create_spinbox(frame,4,'Z:', self.move_vertex)
        frame.grid_columnconfigure(5, weight=1)


    def __create_spinbox(self, frame,column, text, command):
        ttk.Label(frame, text=text).grid(row=0,column=column, padx=2)
        c_vcmd = (self.register(self.on_validate_coord), '%P')
        spinbox = ttk.Spinbox(frame, from_ = -100*self.__N, to = 100*self.__N, state="disabled", command=command, validate='all', validatecommand=c_vcmd)
        spinbox.grid(row=0, column=column+1,padx=2)
        spinbox.bind('<Enter>', command)
        return spinbox
        
       # c_vcmd = self._root.register(self.on_validate_coord, '%P')
    
    def __create_close_button(self):
        ttk.Button(self, text='Close window', command=self.destroy).pack(side='top', expand=True)

    def move_vertex(self, event):
        x,y,z = self.__x_spinbox.get(), self.__y_spinbox.get(), self.__z_spinbox.get()
        if x == '' or y == '' or z == '':
            return
        else:
            self.__vertex.move_to(float(x), float(y), float(z))


    def on_validate_vertex(self, s):
        try:
            #print(s)
            digit = int(s)
            return 0 < digit <= self.__N
        except ValueError:
            return s == ""

    def on_validate_coord(self, c):
        try:
            float(c)
            return True
        except ValueError:
            return c == ""

    def on_focus_in(self, event):
        if not self.__entry_value.get().isdigit():
            self.__entry_value.set("")

    def on_focus_out(self, event):
        if self.__entry_value.get() == '':
            self.__entry_value.set("Input vertex")

    def select_vertex(self):
        s = self.__entry_value.get()
        if s.isdigit():
            v = int(s)
            self.__vertex = self.__graph.give_vertex(v)
            state = "normal"      
        else:
            self.__vertex = None
            state = "disabled"

        self.__x_spinbox.config(state=state)
        self.__y_spinbox.config(state=state)
        self.__z_spinbox.config(state=state)

    def move_x(self):
        x = float(self.__x_value.get())
        self.__vertex.move_x(x)
    
    def move_y(self):
        y = float(self.__y_value.get())
        self.__vertex.move_y(y)

    def move_z(self):
        z = float(self.__z_value.get())
        self.__vertex.move_z(z)




class RotationInterface(ttk.Frame):
    def __init__(self, root, canvas, graph):
        super().__init__(root)
        self.pack(pady=5, fill='x', padx=5)
        self.__canvas = canvas
        self.__graph = graph
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Label(self, text="Rotation").pack()
        self.__create_sliders()
        self.__create_buttons()

    def __create_sliders(self):
        #ttk.Frame()
        self.__create_slider('X:', self.__canvas.x_rot_angle)
        self.__create_slider('Y:', self.__canvas.y_rot_angle)
        self.__create_slider('Z:', self.__canvas.z_rot_angle)

    def __create_slider(self,text, variable):
        slider_frame = ttk.Frame(self)
        slider_frame.pack(pady=2,fill='x')
        ttk.Label(slider_frame, text=text).grid(row=0, column=0, sticky='w',padx=2)
        ttk.Scale(slider_frame, variable=variable, from_=-PI, to=PI, command=self.__canvas.redraw()).grid(row=0, column=1, sticky='ew', padx=2)
        slider_frame.columnconfigure(1, weight=1)
        return

    def __create_buttons(self):
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=1, fill='x')

        ttk.Button(btn_frame, text="Reset", command=self.__reset_rotation).pack(side='right',expand=True)
        ttk.Button(btn_frame, text="Fix", command=self.__fix_rotation).pack(side='right',expand=True)


    def __reset_rotation(self):
        pass

    def __fix_rotation(self):
        pass



class MovingInterface(ttk.Frame):
    def __init__(self, root, canvas):
        super().__init__(root)
        self.pack(pady=5, fill='x', padx=5)
        self.canvas = canvas
        self.__create_move_buttons()

    def __create_move_buttons(self):
        ttk.Button(self, text="⬆", command=self.canvas.move_up).grid(row=0, column=1, pady=5)
        ttk.Button(self, text="⬅", command=self.canvas.move_left).grid(row=1, column=0, pady=5)
        ttk.Button(self, text="⮕", command=self.canvas.move_right).grid(row=1, column=2, pady=5)
        ttk.Button(self, text="⬇", command=self.canvas.move_down).grid(row=2, column=1, pady=5)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)


class Controls(ttk.Frame):
    def __init__(self, root, canvas, graph, relx=0.81, rely=0.01, relwidth=0.19, relheight=0.98, anchor="nw"):
        super().__init__(root)
        self.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight, anchor=anchor)

        self.__canvas = canvas
        self.__graph = graph
        self.__vertex_mover = None
        self.__create_widgets()

    def __create_widgets(self):
        self.__create_vertex_mover_button()
        self.__create_zoom_slider(self.__canvas.zoom)
        self.__create_rotation_interface()
        self.__create_moving_interface()

    def __create_vertex_mover_button(self):
        ttk.Button(self, text='Move vertex', command=self.__create_vertex_mover, state='normal').pack(side='top', pady=2)

        #self._vertex_mover_button.place(relx=0.01, rely=0.09, relwidth=0.15, relheight=0.06, anchor='ne')

    def __create_vertex_mover(self):
        if self.__vertex_mover is None:
            self.__vertex_mover = VertexMover(self, self.__graph)
            self.__vertex_mover.bind("<Destroy>", self.on_vertex_mover_destroy)
        else:
            self.__vertex_mover.lift()

    def on_vertex_mover_destroy(self, event):
        self.__vertex_mover = None

       
    def __create_zoom_slider(self, variable):
        ttk.Label(self, text="Zoom").pack(side='top',pady=(5,3))

        ttk.Scale(self, variable=variable, from_=400.0, to=0.1, orient="horizontal", command=self.__canvas.redraw).pack(pady=3, padx=5, fill='x')


    def __create_rotation_interface(self):
        self.__rotation_interface = RotationInterface(self, self.__canvas, self.__graph)

    def __create_moving_interface(self):
        self.__moving_interface = MovingInterface(self, self.__canvas)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        sv_ttk.set_theme("dark")

        self.__create_widgets()
        self.mainloop()

    def __create_widgets(self):
        self.__create_canvas()
        self.__create_import_button()
        
    def __create_controls(self):
        self.__controls = Controls(self, rely=0.06,relheight=0.92, canvas=self.__canvas, graph=self.__graph)

    def __create_canvas(self):
        self.__canvas = Canvas(self)
       
    def __create_import_button(self):
        ttk.Button(self, text='Import graph', command=self.__import_graph).place(relx=0.905, rely=0.004, relwidth=0.1, relheight=0.05, anchor='n')


    def __import_graph(self):
        filename = tk.filedialog.askopenfilename(defaultextension = ".txt",
                                                 filetypes = (("Text Files", "*.txt"),
                                                              ("All Files", "*.*")))
     #   self.__graph = Graph(filename)
     #   self.__create_controls()
     #   self.__canvas.redraw()


        try:
            self.__graph = Graph(filename)
            self.__create_controls()
            self.__canvas.redraw()
        except Exception as e:
            tk.messagebox.showerror(title=None, message="Некоректні дані")
            #return
            # the next line is for debugging purposes
            self.__graph = Graph()

        self.__create_controls()
        self.__canvas.redraw()


      #  if(self.__graph.read(filename)):
      #      self.__create_controls()
      #      self.__canvas.redraw()
      #  else:
      #      tk.messagebox.showerror(title=None, message="Некоректні дані")


if __name__ == "__main__":
    g = GUI()


