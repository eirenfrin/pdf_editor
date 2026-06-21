from events.observer import Observer
import consts as c
import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageOps
from widgets.pdf_viewer import PdfViewer as Viewer
from widgets.toolbar import Toolbar
from models.pdf_model import PdfModel
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

        self.model = None
        self.pdf_viewer = None
        self.toolbar = Toolbar(self.mainframe, self)

    def canvas_click(self, x, y):
        insert_type = self.toolbar.selected_insert_btn.insert_type
        if self.pdf_viewer.new_text_in_progress:
            if insert_type == c.InsertTypeEnum.NONE:
                self.process_text_entry(c.ClickedTypeEnum.CANVAS_EMPTY)
            else:
                self.process_text_entry(c.ClickedTypeEnum.CANVAS_INSERT)

        if insert_type == c.InsertTypeEnum.ICON:
            img_path = self.toolbar.selected_insert_btn.content
            if img_path not in self.model.icons_inserted_tk_imgs.keys():
                tk_img = self.process_img(img_path, 60, 60) 
                self.model.store_icon_ref(img_path, tk_img)

            icon_model = self.model.generate_icon_model(img_path, x, y)
            icon_id = self.pdf_viewer.insert_icon(x, y, icon_model.tk_img)
            icon_model.set_id(icon_id)
            self.model.store_inserted_icon_model(icon_model)
            self.pdf_viewer.select_element(icon_id, c.InsertTypeEnum.ICON)
        elif insert_type == c.InsertTypeEnum.ENTRY:
            self.pdf_viewer.insert_text_entry(x, y)


    def process_text_entry(self, clicked):
        text_data = self.pdf_viewer.save_inserted_text()
        if text_data.element_id:
            self.model.generate_text_model(text_data)
            # clicked on existing element or on canvas with insert btn active
            if clicked == c.ClickedTypeEnum.CANVAS_INSERT or clicked == c.ClickedTypeEnum.ELEMENT: 
                return
            # clicked Enter key to save text entry result
            elif clicked == c.ClickedTypeEnum.ENTER:
                return text_data
            # clicked on empty canvas with no active btns
            elif clicked == c.ClickedTypeEnum.CANVAS_EMPTY:
                self.pdf_viewer.select_element(text_data.element_id, c.InsertTypeEnum.ENTRY)



    def process_img(self, img_path, width, height):
        img = Image.open(img_path).convert("RGBA")
        img = img.resize((width, height))
        # img = ImageOps.exif_transpose(img)
        tk_img = ImageTk.PhotoImage(img)
        return tk_img
    
    def change_icon_size(self, prop, value):
        icon_model = self.model.icons_models[self.pdf_viewer.selected_element.element_ref]
        new_size = icon_model.update_size(prop, value)
        new_tk_img = self.process_img(icon_model.img_path, *new_size)
        self.model.store_icon_ref(self.pdf_viewer.selected_element.element_ref, new_tk_img)
        icon_model.update_tk_img(new_tk_img)
        self.pdf_viewer.change_icon_size(new_tk_img)

    def change_icon_pos(self, prop, value):
        new_pos = self.model.icons_models[self.pdf_viewer.selected_element.element_ref].update_pos(prop, value)
        self.pdf_viewer.change_icon_pos(*new_pos)
    
    def load_selected_icon_info(self, icon_id):
        icon_model = self.model.icons_models[icon_id]
        self.toolbar.populate_entries(icon_model.get_model_size_pos(), "normal")

    def empty_icon_info(self):
        params = {
            "width": 0,
            "height": 0,
            "canvas_x": 0,
            "canvas_y": 0
        }
        self.toolbar.populate_entries(params, "readonly")

    def open_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Open pdf",
        )

        if file_path.endswith(".pdf"):
            previous_doc = None
            if self.model:
                previous_doc = self.model.doc
            self.model = PdfModel(file_path)
            pdf_params = self.model.get_pdf_params()
            self.model.close_doc(previous_doc)

            self.pdf_viewer = Viewer(self.mainframe, self, pdf_params)

    def load_icon_btn(self):
        file_path = filedialog.askopenfilename(
            title="Add icon",
        )
        if file_path.endswith((".png", ".jpg", ".jpeg")):
            return file_path
        
    def delete_element_model(self):
        element_ref = self.pdf_viewer.selected_element.element_ref
        insert_type = self.pdf_viewer.selected_element.insert_type
        self.model.delete_element_model(element_ref, insert_type)

    def save_pdf(self):
        if self.model.pdf_path:
            for icon in self.model.icons_models.values():
                page = self.model.doc[icon.page]

                y_diff = self.model.page_height*icon.page
                y_coord = icon.canvas_y - y_diff
                cx = icon.canvas_x + icon.width / 2
                cy = y_coord + icon.height / 2
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
                    filename=icon.img_path,
                    keep_proportion=False,
                    rotate = r_angle
                )

            save_path = filedialog.asksaveasfilename(
                title="Save edited pdf",
                defaultextension=".pdf",
                initialfile="edited.pdf",
                filetypes=[("PDF files", "*.pdf")]
            )

            if save_path:
                self.model.doc.save(save_path)
