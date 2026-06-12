import tkinter as tk
from tkinter import ttk

import fitz
import consts as c
import os
from PIL import Image, ImageTk
from widgets.icon_btn import IconBtn as IB

class Toolbar(ttk.Frame):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.grid(column=0, row=0, sticky=tk.N)
        self.btns = []
        self.selected_icon = (None, None)
        self.model = model

        save_btn = ttk.Button(self, text="save pdf", command=self.save_pdf)
        save_btn.grid(column=0, row=0, pady=5)

        txt_btn = ttk.Button(self, text="add text")
        txt_btn.grid(column=0, row=1, pady=5)

        i = 2
        for file in os.listdir(c.input_folder):
            if file.endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(c.input_folder, file)
                img = Image.open(path)
                img = img.resize((60, 60))
                tk_img = ImageTk.PhotoImage(img)

                self.btns.append(IB(self, tk_img, file, i, self))
                i += 1
    
    def track_selected_icon(self, filename, tk_img):
        if self.selected_icon[0] != filename:
            self.selected_icon = (filename, tk_img)
    
    def save_pdf(self):
        for icon in self.model.icons_added.keys():
            for coords in self.model.icons_added[icon]:
                page = self.model.doc[coords[0]]

                y_diff = self.model.page_height*coords[0]
                y_coord = coords[2] - y_diff
                size = 60
                cx = coords[1] + size / 2
                cy = y_coord + size / 2
                # cx, cy = fitz.Point(coords[1], y_coord) * page.derotation_matrix
                cx, cy = fitz.Point(cx, cy) * page.derotation_matrix
                
                rect = fitz.Rect(
                    cx - size/2,
                    cy - size/2,
                    cx + size/2,
                    cy + size/2
                )

                r_angle = 0
                if page.rotation == 90:
                    r_angle = 90
   
                page.insert_image(
                    rect,
                    filename=os.path.join("temp", icon),
                    keep_proportion=False,
                    rotate = r_angle
                )
        self.model.doc.save(os.path.join(c.output_folder, "edited.pdf"))
        self.model.doc.close()
