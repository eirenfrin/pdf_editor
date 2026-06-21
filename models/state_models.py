from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk

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
class TextData():
    element_id: int | None
    text: str | None
    x: float | None
    y: float | None
    