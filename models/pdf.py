import os
import fitz
from PIL import Image, ImageTk
import consts as c
from events.subject import Subject
from models.icon import Icon
from models.text import Text
from models.data_classes import PdfMetadata

class Pdf():
    def __init__(self, pdf_path=""):
        self.pdf_path = pdf_path
        self.doc = None
        self.num_of_pages = None
        self.page_width = None
        self.page_height = None
        self.pdf_pages_tk_imgs = None
        self.pdf_pages_tops_coords = None

        self.icons_models_refs = {}
        self.icons_default_tk_imgs_refs = {}

        self.texts_models_refs = {}

        self.open_pdf()

    def open_pdf(self):
        if self.pdf_path:
            self.doc = fitz.open(self.pdf_path)
            self.set_pdf_metadata()

    def set_pdf_metadata(self):
        self.num_of_pages = len(self.doc)

        page = self.doc[0]  # assumes all pages are the same size
        self.page_width, self.page_height =  self.get_page_size(page)

        self.pdf_pages_tk_imgs = []
        self.pdf_pages_tops_coords = [0]

        for page_num in range(self.num_of_pages):
            y = self.pdf_pages_tops_coords[-1]
            page = self.doc[page_num]

            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            tk_img = ImageTk.PhotoImage(img)

            self.pdf_pages_tk_imgs.append(tk_img)
            y += tk_img.height()
            if y % self.page_height != 0:
                self.close_doc(self.doc)
                print("pages not uniform size")
                return
            self.pdf_pages_tops_coords.append(y)
        self.pdf_pages_tops_coords.pop()

    def get_page_size(self, page):
        pix = page.get_pixmap()
        return (pix.width, pix.height)
    
    def find_page_number(self, y):
        clicked_page_number = 0
        for page in self.pdf_pages_tops_coords[1:]:
            if page > y:
                break
            clicked_page_number += 1
        return clicked_page_number
    
    def get_pdf_params(self):
        return PdfMetadata(self.page_width, self.page_height, self.pdf_pages_tops_coords, self.pdf_pages_tk_imgs)
    
    def close_doc(self, doc):
        if doc:
            doc.close()

    def store_default_icon_img_ref(self, file_path, tk_img):
        self.icons_default_tk_imgs_refs[file_path] = tk_img

    def store_inserted_icon_model(self, icon_model):
        self.icons_models_refs[icon_model.id] = icon_model

    def generate_icon_model(self, file_path, x, y):
        inserted_on_page = self.find_page_number(y)
        new_icon = Icon(file_path, self.icons_default_tk_imgs_refs[file_path], x, y, inserted_on_page)

        return new_icon
    
    def generate_text_model(self, text_snapshot):
        inserted_on_page = self.find_page_number(text_snapshot.canvas_y)
        new_text = Text(text_snapshot.id, text_snapshot.text, inserted_on_page, text_snapshot.canvas_x, text_snapshot.canvas_y)
        self.texts_models_refs[new_text.id] = new_text

    def delete_element_model(self, element_ref, insert_type):
        if insert_type == c.InsertTypeEnum.TEXT:
            self.texts_models_refs.pop(element_ref)
        elif insert_type == c.InsertTypeEnum.ICON:
            self.icons_models_refs.pop(element_ref)


