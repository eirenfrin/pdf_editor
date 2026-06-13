import tkinter as tk
from tkinter import ttk
from widgets.pdf_viewer import PdfViewer as PDFv
from widgets.toolbar import Toolbar as TB
from pdf_model import PdfModel as Model
from edit_manager import EditManager as Manager

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.edit_manager = Manager(self)
