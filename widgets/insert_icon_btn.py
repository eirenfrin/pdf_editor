import tkinter as tk
from tkinter import ttk
import consts as c

class InsertIconBtn(ttk.Frame):
    def __init__(self, parent, tk_img, img_path, row, toolbar):
        self.img_path = img_path
        self.image = tk_img
        self.toolbar = toolbar
        self.row = row

        super().__init__(parent)
        self.grid(column=0, row=row, pady=5)

        self.btn = ttk.Button(self, image=tk_img, command=self.select_icon)
        self.btn.grid(row=0, column=0)

        self.style = ttk.Style()
        self.style.configure(
            "Xdelete.TButton",
            padding=0,
            font=("Arial", 8)
        )

        self.detete_btn = ttk.Button(self, text="✕", width=2, style="Xdelete.TButton", command=self.delete_icon_btn)
        self.detete_btn.place(relx=1.0, rely=0.0, anchor="ne")

    def select_icon(self):
        self.toolbar.toggle_selected_insert_btn(c.InsertType.ICON, self.img_path)

    def delete_icon_btn(self):
        self.toolbar.delete_insert_icon_btn(self.img_path)
        self.destroy()