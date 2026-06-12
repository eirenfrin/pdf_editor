import os
import fitz
from PIL import Image, ImageTk
import consts as c
from events.subject import Subject

class PdfModel(Subject):
    def __init__(self):
        super().__init__()
        self.doc = None
        self.num_of_pages = 0
        self.page_width = 0
        self.page_height = 0
        self.pdf_pages = []
        self.pdf_pages_tops_coords = [0]
        self.icons_added = {}
        self.icons_refs = []

    def create_output_folder(self):
        os.makedirs(c.output_folder, exist_ok=True)
        
    def set_pdf_page_num_size(self):
        pdf_path = os.path.join(c.input_folder, "long.pdf")
        self.doc = fitz.open(pdf_path)
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

    def store_canvas_coords(self, x, y):
        self.canvas_clicked = (x, y)
        self.notify("manager:add_photo", self.canvas_clicked)

    def find_page_number(self):
        clicked_page_number = 0
        for page in self.pdf_pages_tops_coords[1:]:
            if page > self.canvas_clicked[1]:
                break
            clicked_page_number += 1
        return clicked_page_number

    def store_inserted_image_canvas_coords(self, filename, file):
        page_number = self.find_page_number()
        if filename in self.icons_added.keys():
            self.icons_added[filename].append((page_number, *self.canvas_clicked))
        else:
            self.icons_added[filename] = [(page_number, *self.canvas_clicked)]
        self.icons_refs.append(file)
        self.notify("viewer:add_photo", (*self.canvas_clicked, file))
