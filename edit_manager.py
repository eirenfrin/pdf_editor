from events.observer import Observer
import consts as c
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from widgets.pdf_viewer import PdfViewer as Viewer
from widgets.toolbar import Toolbar
from pdf_model import PdfModel
import fitz

class EditManager():
    def __init__(self, root):
        self.root = root

        self.root.title("PDF miniEditor")

        self.mainframe = ttk.Frame(self.root, padding=(3,3,3,3))
        self.mainframe.grid(column=0, row=0)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.update_idletasks()

        self.model = PdfModel()
        pdf_params = self.model.get_pdf_params()

        self.pdf_viewer = Viewer(self.mainframe, self, pdf_params)
        self.toolbar = Toolbar(self.mainframe, self)

    def canvas_click_callback(self, x, y):
        icon_filename = self.toolbar.selected_icon
        if icon_filename:
            if icon_filename not in self.model.icons_inserted_tk_imgs.keys():
                tk_img = self.resize_icon(icon_filename, 60, 60) 
                self.model.store_icon_ref(icon_filename, tk_img)

            icon_model = self.model.generate_icon_model(icon_filename, x, y)
            inserted_id = self.pdf_viewer.insert_icon(x, y, icon_model.tk_img)
            icon_model.set_id(inserted_id)
            self.model.store_inserted_icon_model(icon_model)
            self.pdf_viewer.select_icon(inserted_id)

    def resize_icon(self, filename, width, height):
        path = os.path.join(c.input_folder, filename)
        img = Image.open(path).convert("RGBA")
        img = img.resize((width, height))
        # img = ImageOps.exif_transpose(img)
        tk_img = ImageTk.PhotoImage(img)
        return tk_img
    
    def change_icon_size(self, prop, value):
        icon_model = self.model.icons_models[self.pdf_viewer.selected_icon[0]]
        new_size = icon_model.update_size(prop, value)
        new_tk_img = self.resize_icon(icon_model.filename, *new_size)
        self.model.store_icon_ref(self.pdf_viewer.selected_icon[0], new_tk_img)
        icon_model.update_tk_img(new_tk_img)
        self.pdf_viewer.change_icon_size(new_tk_img)

    def change_icon_pos(self, prop, value):
        new_pos = self.model.icons_models[self.pdf_viewer.selected_icon[0]].update_pos(prop, value)
        self.pdf_viewer.change_icon_pos(*new_pos)
    
    def load_selected_icon_info(self, icon_id):
        icon_model = self.model.icons_models[icon_id]
        self.toolbar.populate_entries(icon_model.get_model_size_pos())

    def save_pdf(self):
        for icon in self.model.icons_models.values():
            page = self.model.doc[icon.page]

            y_diff = self.model.page_height*icon.page
            y_coord = icon.canvas_y - y_diff
            cx = icon.canvas_x + icon.width / 2
            cy = y_coord + icon.height / 2
            # cx, cy = fitz.Point(coords[1], y_coord) * page.derotation_matrix
            cx, cy = fitz.Point(cx, cy) * page.derotation_matrix

            r_angle = 0
            if page.rotation == 0:
                rect = fitz.Rect(
                    cx - icon.width/2,
                    cy - icon.height/2,
                    cx + icon.width/2,
                    cy + icon.height/2
                )
            if page.rotation == 90:
                r_angle = 90
                rect = fitz.Rect(
                    cx - icon.height/2,
                    cy - icon.width/2,
                    cx + icon.height/2,
                    cy + icon.width/2
                )

            page.insert_image(
                rect,
                filename=os.path.join(c.input_folder, icon.filename),
                keep_proportion=False,
                rotate = r_angle
            )
        self.model.doc.save(os.path.join(c.output_folder, "edited.pdf"))
        self.model.doc.close()
