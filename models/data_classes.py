from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

import consts as c

@dataclass
class SelectedInsertBtn():
    insert_type: c.InsertTypeEnum
    content: str

@dataclass
class SelectedCanvasElement():
    insert_type: c.InsertTypeEnum
    element_ref: int | ttk.Entry | None
    border_ref: int | None

@dataclass
class TextSnapshot():
    id: int | None
    text: str | None
    canvas_x: float | None
    canvas_y: float | None

@dataclass
class IconMetadata():
    width: int
    height: int
    canvas_x: float
    canvas_y: float

@dataclass
class TextMetadata():
    font: str
    size: int
    canvas_x: float
    canvas_y: float

@dataclass
class PdfMetadata():
    page_width: int
    page_height: int
    pdf_pages_tops_coords: list[int]
    pdf_pages_tk_imgs: list[ImageTk.PhotoImage]

@dataclass
class EntryVariableMap():
    string_var: tk.StringVar
    entry: ttk.Entry
