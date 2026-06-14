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
        self.btns = []
        self.selected_icon = None

        save_btn = ttk.Button(self, text="save pdf", command=self.save_pdf)
        save_btn.grid(column=0, row=0, pady=5)

        ttk.Label(self, text="x").grid(column=0, row=1, sticky=tk.W)
        self.x = StringVar()
        self.x_entry = ttk.Entry(self, width=7, textvariable=self.x)
        self.x_entry.grid(column=1, row=1)
        self.x_entry.bind("<Return>", self.on_change_x)

        ttk.Label(self, text="y").grid(column=0, row=2, sticky=tk.W)
        self.y = StringVar()
        self.y_entry = ttk.Entry(self, width=7, textvariable=self.y)
        self.y_entry.grid(column=1, row=2)
        self.y_entry.bind("<Return>", self.on_change_y)

        txt_btn = ttk.Button(self, text="add text")
        txt_btn.grid(column=0, row=3, pady=5)

        row_index = 4
        for file in os.listdir(c.input_folder):
            if file.endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(c.input_folder, file)
                img = Image.open(path)
                img = img.resize((60, 60))
                tk_img = ImageTk.PhotoImage(img)

                self.btns.append(IB(self, tk_img, file, row_index, self))
                row_index += 1

    def on_change_x(self, event):
        self.manager.change_icon_params("canvas_x", float(self.x.get()))

    def on_change_y(self, event):
        self.manager.change_icon_params("canvas_y", float(self.y.get()))

    
    def track_selected_icon(self, filename):
        if self.selected_icon == filename:
            self.selected_icon = None
        else:
            self.selected_icon = filename
    
    def populate_entries(self, icon_data):
        self.x.set(icon_data["canvas_x"])
        self.y.set(icon_data["canvas_y"])


    def save_pdf(self):
        self.manager.save_pdf()
