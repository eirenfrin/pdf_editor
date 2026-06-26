from events.observer import Observer
import consts as c
import os
import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk, ImageOps
from widgets.pdf_viewer import PdfViewer as Viewer
from widgets.toolbar import Toolbar
from models.pdf import Pdf
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
        # print(tkfont.families())

    def canvas_click(self, x, y):
        insert_type = self.toolbar.selected_insert_btn.insert_type
        if self.pdf_viewer.new_text_in_progress:
            if insert_type == c.InsertTypeEnum.NONE:
                self.process_text_entry(c.ClickedTypeEnum.CANVAS_EMPTY)
            else:
                self.process_text_entry(c.ClickedTypeEnum.CANVAS_INSERT)

        if insert_type == c.InsertTypeEnum.ICON:
            file_path = self.toolbar.selected_insert_btn.content
            if file_path not in self.model.icons_default_tk_imgs_refs.keys():
                tk_img = self.process_img(file_path, 60, 60) 
                self.model.store_default_icon_img_ref(file_path, tk_img)

            icon_model = self.model.generate_icon_model(file_path, x, y)
            icon_id = self.pdf_viewer.insert_icon(x, y, icon_model.tk_img)
            icon_model.set_id(icon_id)
            self.model.store_inserted_icon_model(icon_model)
            self.pdf_viewer.select_element(icon_id, c.InsertTypeEnum.ICON)
        elif insert_type == c.InsertTypeEnum.ENTRY:
            self.pdf_viewer.insert_text_entry(x, y)

    def process_text_entry(self, clicked):
        text_snapshot = self.pdf_viewer.save_inserted_text()
        if text_snapshot.id:
            self.model.generate_text_model(text_snapshot)
            # clicked on existing element or on canvas with insert btn active
            if clicked == c.ClickedTypeEnum.CANVAS_INSERT or clicked == c.ClickedTypeEnum.ELEMENT: 
                return
            # clicked Enter key to save text entry result
            elif clicked == c.ClickedTypeEnum.ENTER:
                return text_snapshot
            # clicked on empty canvas with no active btns
            elif clicked == c.ClickedTypeEnum.CANVAS_EMPTY:
                self.pdf_viewer.select_element(text_snapshot.id, c.InsertTypeEnum.ENTRY)

    def process_img(self, file_path, width, height):
        img = Image.open(file_path).convert("RGBA")
        img = img.resize((width, height))
        # img = ImageOps.exif_transpose(img)
        tk_img = ImageTk.PhotoImage(img)
        return tk_img
    
    def change_icon_size(self, prop, value):
        icon_model = self.model.icons_models_refs[self.pdf_viewer.selected_element.element_ref]
        icon_model.update_attr(prop, value)
        icon_metadata = icon_model.get_size_pos()
        new_tk_img = self.process_img(icon_model.file_path, icon_metadata.width, icon_metadata.height)
        self.model.store_default_icon_img_ref(self.pdf_viewer.selected_element.element_ref, new_tk_img)
        icon_model.update_attr("tk_img", new_tk_img)
        self.pdf_viewer.change_icon_size(new_tk_img)

    def change_element_pos(self, prop, value):
        element_type = self.pdf_viewer.selected_element.insert_type
        if element_type == c.InsertTypeEnum.ICON:
            icon_model = self.model.icons_models_refs[self.pdf_viewer.selected_element.element_ref]
            icon_model.update_attr(prop, value)
            icon_metadata = icon_model.get_size_pos()
            self.pdf_viewer.change_element_pos(icon_metadata.canvas_x, icon_metadata.canvas_y)
        elif element_type == c.InsertTypeEnum.TEXT:
            text_model = self.model.texts_models_refs[self.pdf_viewer.selected_element.element_ref]
            text_model.update_attr(prop, value)
            text_metadata = text_model.get_style_pos()
            self.pdf_viewer.change_element_pos(text_metadata.canvas_x, text_metadata.canvas_y)

    def change_text_size(self, prop, value):
        text_model = self.model.texts_models_refs[self.pdf_viewer.selected_element.element_ref]
        text_model.update_attr(prop, value)
        text_metadata = text_model.get_style_pos()
        self.pdf_viewer.change_text_size(text_metadata.size)
    
    def load_selected_icon_info(self, icon_id):
        icon_model = self.model.icons_models_refs[icon_id]
        self.toolbar.populate_entries(icon_model.get_size_pos())

    def load_selected_text_info(self, text_id):
        text_model = self.model.texts_models_refs[text_id]
        self.toolbar.populate_entries(text_model.get_style_pos())

    def empty_element_info(self):
        self.toolbar.reset_entries()

    def select_pdf_from_device(self):
        file_path = filedialog.askopenfilename(
            title="Open pdf",
        )

        if file_path.endswith(".pdf"):
            previous_doc = None
            if self.model:
                previous_doc = self.model.doc
            self.model = Pdf(file_path)
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
    
    def load_font(self, page):
        page.insert_font(
            fontname="Arial",
            fontfile="C:/Windows/Fonts/arial.ttf"
        )

    def save_pdf(self):
        if self.model.pdf_path:
            for icon in self.model.icons_models_refs.values():
                page = self.model.doc[icon.page_number]

                y_diff = self.model.page_height*icon.page_number
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
                # elif page.rotation == 90:
                #     r_angle = 90
                #     rect = fitz.Rect(
                #         cx - icon.height/2,
                #         cy - icon.width/2,
                #         cx + icon.height/2,
                #         cy + icon.width/2
                #     )

                page.insert_image(
                    rect,
                    filename=icon.file_path,
                    keep_proportion=False,
                    rotate = r_angle
                )

            for text in self.model.texts_models_refs.values():
                page = self.model.doc[text.page_number]
                self.load_font(page)
                f = tkfont.Font(font=self.pdf_viewer.viewer.itemcget(text.id, "font"))
                ascent = f.metrics("ascent")

                x0, y0, x1, y1 = self.pdf_viewer.viewer.bbox(text.id)
                y_diff = self.model.page_height*text.page_number
                y_coord = y0 - y_diff
                y_corrected = y_coord + ascent
                page.insert_text(
                    (text.canvas_x, y_corrected), 
                    text.content,
                    fontsize=text.size*c.tk_scale,
                    fontname=text.font
                )

            save_path = filedialog.asksaveasfilename(
                title="Save edited pdf",
                defaultextension=".pdf",
                initialfile=c.DEFAULT_OUTPUT_FILENAME,
                filetypes=[("PDF files", "*.pdf")]
            )

            if save_path:
                self.model.doc.save(save_path)
