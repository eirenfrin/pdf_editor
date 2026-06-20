import tkinter as tk
from tkinter import StringVar, ttk

import fitz
import consts as c
import os
from PIL import Image, ImageTk
from widgets.insert_icon_btn import InsertIconBtn as IB

class Toolbar(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager

        self.grid(column=0, row=0, sticky=tk.N)
        self.insert_icon_btns = {}
        self.selected_insert_btn = {
            "insert_type": "",
            "content": ""
        }

        save_pdf_btn = ttk.Button(self, text="save pdf", command=self.save_pdf)
        save_pdf_btn.grid(column=0, row=0, pady=5)

        open_pdf_btn = ttk.Button(self, text="open pdf", command=self.open_pdf)
        open_pdf_btn.grid(column=0, row=1, pady=5)

        self.new_icon_btn = ttk.Button(self, text="add icon", command=self.create_new_icon_btn)
        self.new_icon_btn.grid(column=0, row=2, pady=5)

        ttk.Label(self, text="x").grid(column=0, row=3, sticky=tk.W)
        self.x = StringVar()
        self.x_entry = ttk.Entry(self, width=7, textvariable=self.x)
        self.x_entry.grid(column=1, row=3)
        self.x_entry.bind("<Return>", self.on_change_x)

        ttk.Label(self, text="y").grid(column=0, row=4, sticky=tk.W)
        self.y = StringVar()
        self.y_entry = ttk.Entry(self, width=7, textvariable=self.y)
        self.y_entry.grid(column=1, row=4)
        self.y_entry.bind("<Return>", self.on_change_y)

        ttk.Label(self, text="width").grid(column=0, row=5, sticky=tk.W)
        self.width = StringVar()
        self.width_entry = ttk.Entry(self, width=7, textvariable=self.width)
        self.width_entry.grid(column=1, row=5)
        self.width_entry.bind("<Return>", self.on_change_w)

        ttk.Label(self, text="height").grid(column=0, row=6, sticky=tk.W)
        self.height = StringVar()
        self.height_entry = ttk.Entry(self, width=7, textvariable=self.height)
        self.height_entry.grid(column=1, row=6)
        self.height_entry.bind("<Return>", self.on_change_h)

        insert_txt_btn = ttk.Button(self, text="add text", command=self.select_insert_text_btn)
        insert_txt_btn.grid(column=0, row=7, pady=5)

        self.outer_btns_container = ttk.Frame(self)
        self.outer_btns_container.grid(column=0, row=8, columnspan=2)
        self.btns_canvas_container = tk.Canvas(self.outer_btns_container, height=200, width=100)
        self.btns_canvas_container.grid(row=0, column=0)
        self.inner_btns_container = ttk.Frame(self.btns_canvas_container)

        self.btns_canvas_container.create_window(
            (0, 0),
            window=self.inner_btns_container,
            anchor="nw"  
        )

        self.scrollbar = ttk.Scrollbar(self.outer_btns_container, orient="vertical", command=self.btns_canvas_container.yview)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        
        self.btns_canvas_container.bind("<MouseWheel>", self.on_mousewheel)
        self.inner_btns_container.bind("<MouseWheel>", self.on_mousewheel)
        self.btns_canvas_container.configure(yscrollcommand=self.scrollbar.set)

        self.inner_btns_container.bind(
            "<Configure>",
            lambda e: self.btns_canvas_container.configure(
                scrollregion=self.btns_canvas_container.bbox("all")
            )
        )

        self.row_index = 8

    def on_mousewheel(self, event):
        self.btns_canvas_container.yview_scroll(-event.delta // 120, "units")

    def open_pdf(self):
        self.manager.open_pdf()

    def create_new_icon_btn(self):
        img_path = self.manager.load_icon_btn()
        if img_path in self.insert_icon_btns.keys():
            return
        
        img = Image.open(img_path)
        img = img.resize((60, 60))
        tk_img = ImageTk.PhotoImage(img)
            
        new_btn = IB(self.inner_btns_container, tk_img, img_path, self.row_index, self)
        new_btn.bind("<MouseWheel>", self.on_mousewheel)
        for child in new_btn.winfo_children():
            child.bind("<MouseWheel>", self.on_mousewheel)

        self.insert_icon_btns[img_path] = new_btn
        self.row_index += 1

    def on_change_x(self, event):
        self.manager.change_icon_pos("canvas_x", float(self.x.get()))

    def on_change_y(self, event):
        self.manager.change_icon_pos("canvas_y", float(self.y.get()))

    def on_change_w(self, event):
        self.manager.change_icon_size("width", int(self.width.get()))

    def on_change_h(self, event):
        self.manager.change_icon_size("height", int(self.height.get()))

    def select_insert_text_btn(self):
        self.toggle_selected_insert_btn(c.InsertType.TEXT, "")

    def toggle_selected_insert_btn(self, insert_type, content):
        if (self.selected_insert_btn["content"] == content and insert_type == c.InsertType.ICON) or self.selected_insert_btn["insert_type"] == c.InsertType.TEXT == insert_type:
            self.selected_insert_btn["insert_type"] = ""
            self.selected_insert_btn["content"] = ""
        else:
            self.selected_insert_btn["insert_type"] = insert_type
            self.selected_insert_btn["content"] = content
    
    def populate_entries(self, icon_data, state):
        self.x.set(icon_data["canvas_x"])
        self.y.set(icon_data["canvas_y"])
        self.width.set(icon_data["width"])
        self.height.set(icon_data["height"])
        self.x_entry.configure(state=state)
        self.y_entry.configure(state=state)
        self.height_entry.configure(state=state)
        self.width_entry.configure(state=state)

    def save_pdf(self):
        self.manager.save_pdf()

    def delete_insert_icon_btn(self, img_path):
        if self.selected_insert_btn["content"] == img_path:
            self.selected_insert_btn["insert_type"] = ""
            self.selected_insert_btn["content"] = ""
        self.insert_icon_btns.pop(img_path)