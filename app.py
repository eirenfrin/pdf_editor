import tkinter as tk
from tkinter import ttk
from widgets.pdf_viewer import PdfViewer as PDFv
from widgets.toolbar import Toolbar as TB
from pdf_model import PdfModel as PDFm
from edit_manager import EditManager as EM
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF miniEditor")

        self.mainframe = ttk.Frame(self, padding=(3,3,3,3))
        self.mainframe.grid(column=0, row=0)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.update_idletasks()

        self.model = PDFm()
        self.model.create_output_folder()
        self.model.set_pdf_page_num_size()
        self.model.store_pages()

        self.pdf_viewer = PDFv(self, self.model)
        self.toolbar = TB(self, self.model)
        self.edit_manager = EM(self.model, self.toolbar)

        self.model.add_observer(self.pdf_viewer)
        self.model.add_observer(self.edit_manager)