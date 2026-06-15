import os
import fitz
from PIL import Image, ImageTk
import consts as c
from events.subject import Subject
from icon_model import IconModel

class PdfModel():
    def __init__(self, pdf_path=""):
        super().__init__()
        self.pdf_path = pdf_path
        self.doc = None
        self.num_of_pages = 0
        self.page_width = 0
        self.page_height = 0
        self.pdf_pages = []
        self.pdf_pages_tops_coords = [0]

        self.icons_models = {}
        self.icons_inserted_tk_imgs = {}

        self.create_output_folder()
        self.set_pdf_page_num_size()
        self.store_pages()

    def create_output_folder(self):
        os.makedirs(c.output_folder, exist_ok=True)
        
    def set_pdf_page_num_size(self):
        if self.pdf_path:
            self.doc = fitz.open(self.pdf_path)
            self.num_of_pages = len(self.doc)

            page = self.doc[0]
            pix = page.get_pixmap()
            self.page_width = pix.width
            self.page_height = pix.height

    def store_pages(self):
        for page_num in range(self.num_of_pages):
            y = self.pdf_pages_tops_coords[-1]
            page = self.doc[page_num]

            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            tk_img = ImageTk.PhotoImage(img)

            self.pdf_pages.append(tk_img)
            y += tk_img.height()
            self.pdf_pages_tops_coords.append(y)
        self.pdf_pages_tops_coords.pop()

    def store_icon_ref(self, filename, tk_img):
        self.icons_inserted_tk_imgs[filename] = tk_img

    def store_inserted_icon_model(self, icon_model):
        self.icons_models[icon_model.inserted_id] = icon_model

    def generate_icon_model(self, filename, x, y):
        inserted_on_page = self.find_page_number(y)
        new_icon = IconModel(filename, self.icons_inserted_tk_imgs[filename], x, y, inserted_on_page)

        return new_icon

    def find_page_number(self, y):
        clicked_page_number = 0
        for page in self.pdf_pages_tops_coords[1:]:
            if page > y:
                break
            clicked_page_number += 1
        return clicked_page_number
    
    def get_pdf_params(self):
        return {
            "page_width": self.page_width,
            "page_height": self.page_height,
            "pdf_pages_tops_coords": self.pdf_pages_tops_coords,
            "pdf_pages": self.pdf_pages
        }
    
    def close_doc(self, doc):
        if doc:
            doc.close()

