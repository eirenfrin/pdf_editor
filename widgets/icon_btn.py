import tkinter as tk
from tkinter import ttk

class IconBtn(ttk.Frame):
    def __init__(self, parent, tk_img, img_path, r, toolbar):
        self.img_path = img_path
        self.image = tk_img
        self.toolbar = toolbar
        self.row = r
        super().__init__(parent)
        self.grid(column=0, row=r, pady=5)

        self.btn = ttk.Button(self, image=tk_img, command=self.select_icon)
        self.btn.grid(row=0, column=0)

        style = ttk.Style()

        style.configure(
            "Small.TButton",
            padding=0,
            font=("Arial", 8)
        )


        self.detete_btn = ttk.Button(self, text="✕", width=2, style="Small.TButton", command=self.delete_icon_btn)
        self.detete_btn.place(relx=1.0, rely=0.0, anchor="ne")

        # self.style = ttk.Style()

    def select_icon(self):
        self.toolbar.track_selected_icon(self.img_path)

    def delete_icon_btn(self):
        self.toolbar.delete_icon_btn(self.img_path)
        self.destroy()