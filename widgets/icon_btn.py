import tkinter as tk
from tkinter import ttk

class IconBtn(ttk.Button):
    def __init__(self, parent, tk_img, file, r, toolbar):
        self.icon_filename = file
        self.image = tk_img
        self.toolbar = toolbar
        super().__init__(parent, image=tk_img, command=self.select_icon)
        self.grid(column=0, row=r, pady=5)

    def select_icon(self):
        self.toolbar.track_selected_icon(self.icon_filename, self.image)