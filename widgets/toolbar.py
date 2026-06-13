import tkinter as tk
from tkinter import ttk

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

        txt_btn = ttk.Button(self, text="add text")
        txt_btn.grid(column=0, row=1, pady=5)

        row_index = 2
        for file in os.listdir(c.input_folder):
            if file.endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(c.input_folder, file)
                img = Image.open(path)
                img = img.resize((60, 60))
                tk_img = ImageTk.PhotoImage(img)

                self.btns.append(IB(self, tk_img, file, row_index, self))
                row_index += 1
    
    def track_selected_icon(self, filename):
        if self.selected_icon != filename:
            self.selected_icon = filename
    
    def save_pdf(self):
        self.manager.save_pdf()
