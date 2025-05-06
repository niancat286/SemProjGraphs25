import tkinter as tk
from tkinter import ttk, filedialog
from graph import Graph
from canvas import Canvas
import sv_ttk

PI = 3.1415926535

class VertexMover(tk.Toplevel):
    def __init__(self, root, graph, N=15):
        super().__init__(root)
        
        self.title("Move Vertex")
        self.geometry("400x300")
        self.geometry("-100-100")
        #self.__root.protocol("WM_DELETE_WINDOW", self.__hide)
        #self.__root.withdraw()

        self.__graph = graph
        self.__N = N
#        self.__N = graph.N
        self.__vertex = None
        
        self.__create_widgets()

    def __create_widgets(self):
        self.__create_entry()

        self.__create_choose_button()
        self.__create_x_spinbox()
        self.__create_y_spinbox()
        self.__create_z_spinbox()
        self.__create_close_button()

    def __create_entry(self):
        self.__entry_value = tk.StringVar(value="Input vertex")
        v_vcmd = (self.register(self.on_validate_vertex), '%P')
        self.__vertex_entry = ttk.Entry(self, textvariable = self.__entry_value, validate="all", validatecommand=v_vcmd)
        self.__vertex_entry.place(relx=0.02, rely=0.02, relwidth=0.45, relheight=0.2, anchor='nw')
        self.__vertex_entry.bind("<FocusIn>", self.on_focus_in)
        self.__vertex_entry.bind("<FocusOut>", self.on_focus_out)
        
    def __create_choose_button(self):
        self.__choose_button = ttk.Button(self, text="Choose")
        self.__choose_button.place(relx=0.5, rely=0.02, relwidth=0.45, relheight=0.2, anchor='nw')
        self.__choose_button['command'] = self.select_vertex

       # c_vcmd = self._root.register(self.on_validate_coord, '%P')
    def __create_x_spinbox(self):
        self.__x_label = ttk.Label(self, text="X:")
        self.__x_value = tk.StringVar(value = 0)
        self.__x_spinbox = ttk.Spinbox(self, textvariable=self.__x_value, from_ = -100*self.__N, to = 100*self.__N, state="disabled", command=self.move_x)
    
        self.__x_label.place(relx = 0.04, rely = 0.3, relwidth = 0.3, relheight=0.1, anchor='nw')
        self.__x_spinbox.place(relx = 0.32, rely = 0.3, relwidth = 0.3, relheight = 0.1, anchor='nw')

    def __create_y_spinbox(self):
        self.__y_label = ttk.Label(self, text="Y:")
        self.__y_value = tk.StringVar(value = 0)
        self.__y_spinbox = ttk.Spinbox(self, textvariable=self.__y_value, from_ = -100*self.__N, to = 100*self.__N, state="disabled", command=self.move_y)
        
        self.__y_label.place(relx = 0.04, rely = 0.41, relwidth = 0.3, relheight=0.1, anchor='nw')
        self.__y_spinbox.place(relx = 0.32, rely = 0.41, relwidth = 0.3, relheight = 0.1, anchor='nw')
    
    def __create_z_spinbox(self):
        self.__z_label = ttk.Label(self, text="Z:")
        self.__z_value = tk.StringVar(value = 0)
        self.__z_spinbox = ttk.Spinbox(self, textvariable=self.__z_value, from_ = -100*self.__N, to = 100*self.__N, state="disabled",command=self.move_z)
        
        self.__z_label.place(relx = 0.04, rely = 0.52, relwidth = 0.03, relheight=0.1, anchor='nw')
        self.__z_spinbox.place(relx = 0.32, rely = 0.52, relwidth = 0.3, relheight = 0.1, anchor='nw')
    
    def __create_close_button(self):
        self.__close_button = ttk.Button(self, text='Close window', command=self.destroy)
        self.__close_button.place(relx=0.5, rely = 0.8, relwidth = 0.5, relheight=0.1, anchor='center')

    def on_validate_vertex(self, s):
        try:
            print(s)
            digit = int(s)
            return 0 < digit <= self.__N
        except ValueError:
            return s == ""

    def on_validate_coord(self, c):
        try:
            float(c)
            return True
        except ValueError:
            return False

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
            self.__x_value.set(self.__vertex.x)
            self.__y_value.set(self.__vertex.y)
            self.__z_value.set(self.__vertex.z)

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
        self.__label = ttk.Label(self, text="Rotation")
        self.__label.pack()
        self.__create_sliders()
        self.__create_buttons()

    def __create_sliders(self):
        #ttk.Frame()
        self.__x_rot_slider = self.__create_slider('X:', self.__canvas.x_rot_angle)
        self.__y_rot_slider = self.__create_slider('Y:', self.__canvas.y_rot_angle)
        self.__z_rot_slider = self.__create_slider('Z:', self.__canvas.z_rot_angle)

    def __create_slider(self,text, variable):
        slider_frame = ttk.Frame(self)
        slider_frame.pack(pady=2,fill='x')
        ttk.Label(slider_frame, text=text).grid(row=0, column=0, sticky='w',padx=2)
        slider = ttk.Scale(slider_frame, variable=variable, from_=-PI, to=PI, command=self.__canvas.redraw())
        slider.grid(row=0, column=1, sticky='ew', padx=2)
        slider.set(0)
        slider_frame.columnconfigure(1, weight=1)
        return slider




    def __create_buttons(self):
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=1, fill='x')

        self.__reset_button = ttk.Button(btn_frame, text="Reset", command=self.__reset_rotation)
   #     self.__reset_button.grid(row=0,column=1,sticky='e')
        self.__reset_button.pack(side='right',expand=True)

        self.__fix_button = ttk.Button(btn_frame, text="Fix", command=self.__fix_rotation)
   #     self.__fix_button.grid(row=0,column=0,sticky='w')
        self.__fix_button.pack(side='right',expand=True)
        pass

    def __reset_rotation(self):
        pass

    def __fix_rotation(self):
        pass






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

    def __create_vertex_mover_button(self):
        self.__vertex_mover_button = ttk.Button(self, text='Move vertex', command=self.__create_vertex_mover, state='normal')
        self.__vertex_mover_button.pack(side='top', pady=2)
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
        self.__zoom_label = ttk.Label(self, text="Zoom")
        self.__zoom_label.pack(side='top',pady=(5,3))
        self.__zoom_slider = ttk.Scale(self, variable=variable, from_=400.0, to=0.1, orient="horizontal", command=self.__canvas.redraw)
        self.__zoom_slider.set(2)#canvas.zoom
        self.__zoom_slider.pack(pady=3, padx=5, fill='x')


    def __create_rotation_interface(self):
        self.__rotation_interface = RotationInterface(self, self.__canvas, self.__graph)
       

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        sv_ttk.set_theme("dark")
        self.__graph = Graph()

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
        self.__import_graph_button = ttk.Button(self, text='Import graph', command=self.__import_graph)
        self.__import_graph_button.place(relx=0.905, rely=0.004, relwidth=0.1, relheight=0.05, anchor='n')

    def __import_graph(self):
        filename = tk.filedialog.askopenfilename(defaultextension = ".txt",
                                                 filetypes = (("Text Files", "*.txt"),
                                                              ("All Files", "*.*")))

        if(self.__graph.read(filename)):
            self.__create_controls()
            self.__canvas.redraw()
        else:
            self.messagebox.showerror(title=None, message="Некоректні дані")


if __name__ == "__main__":
    g = GUI()


