import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Frame(tk.Frame):
    def __init__(self, parent, width: int, height: int):
        super().__init__(parent, width=width, height=height, borderwidth=3, relief="groove")


class Label(tk.Label):
    def __init__(self, parent, text: str, size: int):
        super().__init__(parent, text=text, font=("Helvetica", size))


class Tab(ttk.Frame):
    def __init__(self, parent, width: int, height: int):
        super().__init__(parent, width=width, height=height, borderwidth=3, relief="ridge")


class CGSystemInterface():
    def __init__(self, system):
        self.menu_frame            : Frame
        self.object_menu_frame     : Frame
        self.controls_menu_frame   : Frame
        self.rotation_menu_frame   : Frame
        self.canvas_frame          : Frame
        self.messageBox_frame      : Frame
        self.messageBox            : tk.Listbox
        self.objects_listbox       : tk.Listbox
        self.canvas                : tk.Canvas
        self.w_offset_var          : tk.IntVar
        self.obj_offset_var        : tk.IntVar
        self.w_zoom_factor_var     : tk.DoubleVar
        self.obj_zoom_factor_var   : tk.DoubleVar
        self.rotation_opt_var      : tk.StringVar
        self.window_degrees_var    : tk.DoubleVar
        self.object_degrees_var    : tk.DoubleVar
        self.obj_rotation_coord_var: tuple[tk.IntVar, tk.IntVar]
        self.Wcoord_var            : tuple[tk.IntVar, tk.IntVar]
        self.canvas_width          : int
        self.canvas_height         : int
        self.tab_width             : int
        self.tab_height            : int
        self.rotation_Xpoint_entry : tk.Entry
        self.rotation_Ypoint_entry : tk.Entry
        self.obj_center_rb         : tk.Radiobutton
        self.origin_rb             : tk.Radiobutton
        self.other_rb              : tk.Radiobutton
        self.controls_menu_tab     : ttk.Notebook
        self.window_controls_tab   : Tab
        self.obj_controls_tab      : Tab

        self.app = tk.Tk()
        self.app.title("Computer Graphics System")
        self.app.geometry("1000x700")
        self.system = system

        self.add_menu()
        self.add_canvas()
        self.add_messagesBox()


    def add_canvas(self):
        self.app.update()

        self.canvas_frame = Frame(self.app, self.app.winfo_width()-self.menu_frame.winfo_width()-20, 500)
        self.canvas_frame.place(x=self.menu_frame.winfo_width()+20, y=10)

        Label(self.canvas_frame, "Viewport", 15).place(x=10, y=10)

        self.app.update()
        self.canvas_width = self.canvas_frame.winfo_width()-35
        self.canvas_height = self.canvas_frame.winfo_height()-70
        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white", borderwidth=5, relief="groove")
        self.canvas.place(x=10, y=30)

    def clear_canvas(self):
        self.canvas.delete("all")

    def add_menu(self):
        self.app.update()
        self.menu_frame = Frame(self.app, 300, self.app.winfo_height()-20)
        self.menu_frame.place(x=10, y=10)

        self.app.update()
        self.add_object_menu()
        self.add_controls_tab()


    def add_object_menu(self):
        self.object_menu_frame = Frame(self.menu_frame, self.menu_frame.winfo_width()-26, 180)
        self.object_menu_frame.place(x=10, y=10)

        Label(self.object_menu_frame, "Objects", 10).place(x=10, y=10)

        self.app.update()
        self.objects_listbox = tk.Listbox(self.object_menu_frame, width=self.object_menu_frame.winfo_width()-235, height=6)
        self.objects_listbox.place(x=10, y=30)

        tk.Button(self.object_menu_frame, text="Add", command=self.system.add_object).place(x=45, y=135)
        tk.Button(self.object_menu_frame, text="Del", command=self.del_object).place(x=145, y=135)


    def add_controls_tab(self):
        self.app.update()
        self.controls_menu_tab = ttk.Notebook(self.menu_frame)

        self.tab_width = self.menu_frame.winfo_width()-26
        self.tab_height = self.menu_frame.winfo_height()-self.object_menu_frame.winfo_height()-50

        self.add_window_tab_elements()
        self.add_object_tab_elements()

        self.controls_menu_tab.place(x=10, y=self.object_menu_frame.winfo_height()+15)


    def add_window_tab_elements(self):
        self.window_controls_tab = Tab(self.controls_menu_tab, width=self.tab_width, height=self.tab_height)

        self.add_controls_menu(isObject=False)
        self.add_window_rotation_menu()

        self.controls_menu_tab.add(self.window_controls_tab, text="Window")

    def add_object_tab_elements(self):
        self.obj_controls_tab = Tab(self.controls_menu_tab, width=self.tab_width, height=self.tab_height)

        self.add_controls_menu(isObject=True)
        self.add_obj_rotation_menu()

        self.controls_menu_tab.add(self.obj_controls_tab, text="Object")

    def add_controls_menu(self, isObject: bool):
        # if isObject == True then "object controls" else "window controls"

        parent = self.obj_controls_tab if (isObject) else self.window_controls_tab

        self.controls_menu_frame = Frame(parent, self.tab_width-26, 220)
        self.controls_menu_frame.place(x=10, y=10)

        Label(self.controls_menu_frame, "Controls", 10).place(x=10, y=10)

        tk.Button(self.controls_menu_frame, text="Up", command=lambda: self.move_up(isObject)).place(x=40, y=40)
        tk.Button(self.controls_menu_frame, text="Left", command=lambda: self.move_left(isObject)).place(x=10, y=70)
        tk.Button(self.controls_menu_frame, text="Right", command=lambda: self.move_right(isObject)).place(x=62, y=70)
        tk.Button(self.controls_menu_frame, text="Down", command=lambda: self.move_down(isObject)).place(x=30, y=100)

        tk.Button(self.controls_menu_frame, text="Zoom In", command=lambda: self.zoom_in(isObject)).place(x=150, y=50)
        tk.Button(self.controls_menu_frame, text="Zoom Out", command=lambda: self.zoom_out(isObject)).place(x=150, y=90)

        tk.Button(self.controls_menu_frame, text="Set Coord", command=self.set_window_coord).place(x=80, y=170)

        Label(self.controls_menu_frame, "offset", 10).place(x=10, y=140)
        self.obj_offset_var = tk.IntVar()
        self.w_offset_var = tk.IntVar()
        self.obj_offset_var.set(10)
        self.w_offset_var.set(10)
        tv = self.obj_offset_var if (isObject) else self.w_offset_var
        tk.Entry(self.controls_menu_frame, textvariable=tv, width=4).place(x=50, y=140)

        Label(self.controls_menu_frame, "zoom factor", 10).place(x=115, y=140)
        self.obj_zoom_factor_var = tk.DoubleVar()
        self.w_zoom_factor_var = tk.DoubleVar()
        self.obj_zoom_factor_var.set(2.0)
        self.w_zoom_factor_var.set(2.0)
        tv = self.obj_zoom_factor_var if (isObject) else self.w_zoom_factor_var
        tk.Entry(self.controls_menu_frame, textvariable=tv, width=4).place(x=200, y=140)


    def add_window_rotation_menu(self):
        self.rotation_menu_frame = Frame(self.window_controls_tab, self.tab_width-26,110)
        self.rotation_menu_frame.place(x=10, y=240)

        Label(self.rotation_menu_frame, "Rotation", 10).place(x=10, y=10)

        self.window_degrees_var = tk.DoubleVar()
        Label(self.rotation_menu_frame, "Degrees", 10).place(x=10, y=50)
        tk.Entry(self.rotation_menu_frame, textvariable=self.window_degrees_var, width=4).place(x=60, y=50)

        tk.Button(self.rotation_menu_frame, text="Anti-ClockWise", command=lambda: self.rotation(False, True)).place(x=110, y=25)
        tk.Button(self.rotation_menu_frame, text="ClockWise", command=lambda: self.rotation(False, False)).place(x=110, y=65)


    def add_obj_rotation_menu(self):
        self.rotation_menu_frame = Frame(self.obj_controls_tab, self.tab_width-26,150)
        self.rotation_menu_frame.place(x=10, y=240)

        Label(self.rotation_menu_frame, "Rotation", 10).place(x=10, y=10)

        self.object_degrees_var = tk.DoubleVar()
        self.object_degrees_var.set(10.)
        Label(self.rotation_menu_frame, "Degrees", 10).place(x=10, y=35)
        tk.Entry(self.rotation_menu_frame, textvariable=self.object_degrees_var, width=4).place(x=60, y=35)

        self.obj_rotation_coord_var = (tk.IntVar(), tk.IntVar())
        Label(self.rotation_menu_frame, "X:", 10).place(x=100, y=35)
        Label(self.rotation_menu_frame, "Y:", 10).place(x=170, y=35)
        self.rotation_Xpoint_entry = tk.Entry(self.rotation_menu_frame, textvariable=self.obj_rotation_coord_var[0], state="disabled", width=4)
        self.rotation_Xpoint_entry.place(x=120, y=35)
        self.rotation_Ypoint_entry = tk.Entry(self.rotation_menu_frame, textvariable=self.obj_rotation_coord_var[1], state="disabled", width=4)
        self.rotation_Ypoint_entry.place(x=190, y=35)

        self.rotation_opt_var = tk.StringVar(self.rotation_menu_frame, "Origin")
        self.obj_center_rb = tk.Radiobutton(self.rotation_menu_frame, text="Obj Center", variable=self.rotation_opt_var, value="Obj Center", command=self.rotation_point_entry_state)
        self.origin_rb = tk.Radiobutton(self.rotation_menu_frame, text="Origin", variable=self.rotation_opt_var, value="Origin", command=self.rotation_point_entry_state)
        self.other_rb = tk.Radiobutton(self.rotation_menu_frame, text="Other", variable=self.rotation_opt_var, value="Other", command=self.rotation_point_entry_state)
        self.obj_center_rb.place(x=20, y=65)
        self.origin_rb.place(x=100, y=65)
        self.other_rb.place(x=160, y=65)

        tk.Button(self.rotation_menu_frame, text="Anti-ClockWise", command=lambda: self.rotation(True, True)).place(x=10, y=100)
        tk.Button(self.rotation_menu_frame, text="ClockWise", command=lambda: self.rotation(True, False)).place(x=150, y=100)


    def rotation_point_entry_state(self):
        if (self.rotation_opt_var.get() == "Other"):
            self.rotation_Xpoint_entry.config(state="normal")
            self.rotation_Ypoint_entry.config(state="normal")
        else:
            self.rotation_Xpoint_entry.config(state="disabled")
            self.rotation_Ypoint_entry.config(state="disabled")


    def del_object(self):
        tp = self.objects_listbox.curselection()
        if (not tp):
            self.send_error("Select an item", "Please select an item to delte!")
            return

        id = tp[0]
        self.system.del_object(id)


    def set_window_coord(self):
        app = tk.Toplevel()
        app.title("Set Coordinates")
        app.geometry("180x150")

        Label(app, "Coordinates", 10).place(x=10, y=10)

        fm = Frame(app, width=160, height=50)
        fm.place(x=10, y=30)

        self.Wcoord_var = (tk.IntVar(), tk.IntVar())

        Label(fm, "X:", 10).place(x=10, y=15)
        tk.Entry(fm, textvariable=self.Wcoord_var[0], width=4).place(x=30, y=10)
        Label(fm, "Y:", 10).place(x=80, y=15)
        tk.Entry(fm, textvariable=self.Wcoord_var[1], width=4).place(x=100, y=10)

        tk.Button(app, text="Set", command=self.set_Wcoord).place(x=20, y=90)
        tk.Button(app, text="Cancel", command=app.destroy).place(x=80, y=90)


    def set_Wcoord(self):
        coord_x = self.verify_num_entry(self.Wcoord_var[0])
        coord_y = self.verify_num_entry(self.Wcoord_var[1])

        if (coord_x is not None) and (coord_y is not None):
            self.system.set_window_coord((coord_x, coord_y))


    def add_messagesBox(self):
        self.app.update()
        width = self.app.winfo_width()-self.menu_frame.winfo_width()-20
        height = self.app.winfo_height()-self.canvas_frame.winfo_height()-30
        self.messageBox_frame = Frame(self.app, width, height)
        self.messageBox_frame.place(x=self.menu_frame.winfo_width()+20, y=self.canvas_frame.winfo_height()+20)

        self.app.update()
        self.messageBox = tk.Listbox(self.messageBox_frame, width=self.messageBox_frame.winfo_width()-575, height=10)
        self.messageBox.place(x=10, y=10)


    def rotation(self, isObject: bool, antiClockwise: bool):
        # if isObject == True then move object else move window

        degrees = self.verify_num_entry(self.object_degrees_var) if (object) else self.verify_num_entry(self.window_degrees_var)
        if (degrees is None):
            return

        if (not isObject):
            self.system.rotate(False, antiClockwise, degrees, None, None, None)
            return

        selected = self.objects_listbox.curselection()
        if (not selected):
            self.send_error("Object not selected", "Please select an object!")
            return

        rotation_opt = self.rotation_opt_var.get()
        obj_id = selected[0]

        if (rotation_opt == "Other"):
            coord_x = self.verify_num_entry(self.obj_rotation_coord_var[0])
            coord_y = self.verify_num_entry(self.obj_rotation_coord_var[1])

            if (coord_x is None) or (coord_y is None):
                return

        else:
            coord_x = 0
            coord_y = 0

        self.system.rotate(True, antiClockwise, degrees, obj_id, rotation_opt, (coord_x, coord_y))


    def move_up(self, isObject: bool):
        var = self.obj_offset_var if (isObject) else self.w_offset_var
        self.verify_move(var, self.system.move_up, isObject)

    def move_down(self, isObject: bool):
        var = self.obj_offset_var if (isObject) else self.w_offset_var
        self.verify_move(var, self.system.move_down, isObject)

    def move_left(self, isObject: bool):
        var = self.obj_offset_var if (isObject) else self.w_offset_var
        self.verify_move(var, self.system.move_left, isObject)

    def move_right(self, isObject: bool):
        var = self.obj_offset_var if (isObject) else self.w_offset_var
        self.verify_move(var, self.system.move_right, isObject)

    def zoom_in(self, isObject: bool):
        var = self.obj_zoom_factor_var if (isObject) else self.w_zoom_factor_var
        self.verify_move(var, self.system.zoom_in, isObject)

    def zoom_out(self, isObject: bool):
        var = self.obj_zoom_factor_var if (isObject) else self.w_zoom_factor_var
        self.verify_move(var, self.system.zoom_out, isObject)

    def verify_num_entry(self, entry) -> int|None:
        try:
            value = entry.get()
        except Exception:
            self.send_error("Value Error", "Please enter a numeric value on entry")
        else:
            return value


    def verify_move(self, variable: tk.IntVar|tk.DoubleVar, func, isObject: bool):
        var = self.verify_num_entry(variable)
        if (var is None):
            return

        if (not isObject):
            func(var, isObject, None)
            return

        selected=self.objects_listbox.curselection()
        if (not selected):
            self.send_error("Object not selected", "Please select an object")
            return

        object_id = selected[0]
        func(var, object, object_id)


    def send_error(self, title: str, message: str):
        messagebox.showerror(title, message)

