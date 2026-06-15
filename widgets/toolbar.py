import tkinter as tk
from tkinter import StringVar, ttk

import fitz
import consts as c
import os
from PIL import Image, ImageTk
from widgets.icon_btn import IconBtn as IB

class Toolbar(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager

        self.grid(column=0, row=0, sticky=tk.N)
        self.btns = {}
        self.selected_icon = None

        save_btn = ttk.Button(self, text="save pdf", command=self.save_pdf)
        save_btn.grid(column=0, row=0, pady=5)

        save_btn = ttk.Button(self, text="open pdf", command=self.open_pdf)
        save_btn.grid(column=0, row=1, pady=5)

        self.add_icon_btn = ttk.Button(self, text="add icon", command=self.add_icon_btn)
        self.add_icon_btn.grid(column=0, row=2, pady=5)

        ttk.Label(self, text="x").grid(column=0, row=3, sticky=tk.W)
        self.x = StringVar()
        self.x_entry = ttk.Entry(self, width=7, textvariable=self.x)
        self.x_entry.grid(column=1, row=3)
        self.x_entry.bind("<Return>", self.on_change_x)

        ttk.Label(self, text="y").grid(column=0, row=4, sticky=tk.W)
        self.y = StringVar()
        self.y_entry = ttk.Entry(self, width=7, textvariable=self.y)
        self.y_entry.grid(column=1, row=4)
        self.y_entry.bind("<Return>", self.on_change_y)

        ttk.Label(self, text="width").grid(column=0, row=5, sticky=tk.W)
        self.width = StringVar()
        self.width_entry = ttk.Entry(self, width=7, textvariable=self.width)
        self.width_entry.grid(column=1, row=5)
        self.width_entry.bind("<Return>", self.on_change_w)

        ttk.Label(self, text="height").grid(column=0, row=6, sticky=tk.W)
        self.height = StringVar()
        self.height_entry = ttk.Entry(self, width=7, textvariable=self.height)
        self.height_entry.grid(column=1, row=6)
        self.height_entry.bind("<Return>", self.on_change_h)

        txt_btn = ttk.Button(self, text="add text")
        txt_btn.grid(column=0, row=7, pady=5)

        # self.outer_btns_container = ttk.Frame(self)
        # self.outer_btns_container.grid(column=0, row=8, columnspan=2)
        # self.btns_canvas_container = tk.Canvas(self.outer_btns_container)
        # self.btns_canvas_container.grid(row=0, column=0)
        
        # self.inner_btns_container = ttk.Frame(self.btns_canvas_container, borderwidth=2, relief="solid")

        # self.btns_canvas_container.create_window(
        #     (0, 0),
        #     window=self.inner_btns_container,
        #     anchor="nw"
        # )

        # self.scrollbar = ttk.Scrollbar(self.outer_btns_container, orient="vertical", command=self.btns_canvas_container.yview)
        # self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        
        # self.btns_canvas_container.bind("<MouseWheel>", self.on_mousewheel)
        # self.btns_canvas_container.configure(yscrollcommand=self.scrollbar.set, scrollregion=self.btns_canvas_container.bbox("all"))

        self.row_index = 8

    def on_mousewheel(self, event):
        self.btns_canvas_container.yview_scroll(-event.delta // 120, "units")

    def open_pdf(self):
        self.manager.open_pdf()

    def add_icon_btn(self):
        print("added")
        image_path = self.manager.add_icon_btn()
        if image_path in self.btns.keys():
            return
        
        img = Image.open(image_path)
        img = img.resize((60, 60))
        tk_img = ImageTk.PhotoImage(img)
            
        self.btns[image_path] = IB(self, tk_img, image_path, self.row_index)
        self.row_index += 1

    def on_change_x(self, event):
        self.manager.change_icon_pos("canvas_x", float(self.x.get()))

    def on_change_y(self, event):
        self.manager.change_icon_pos("canvas_y", float(self.y.get()))

    def on_change_w(self, event):
        self.manager.change_icon_size("width", int(self.width.get()))

    def on_change_h(self, event):
        self.manager.change_icon_size("height", int(self.height.get()))

    def track_selected_icon(self, filename):
        if self.selected_icon == filename:
            self.selected_icon = None
        else:
            self.selected_icon = filename
    
    def populate_entries(self, icon_data):
        self.x.set(icon_data["canvas_x"])
        self.y.set(icon_data["canvas_y"])
        self.width.set(icon_data["width"])
        self.height.set(icon_data["height"])

    def save_pdf(self):
        self.manager.save_pdf()
