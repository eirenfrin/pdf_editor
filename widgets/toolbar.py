import tkinter as tk
from tkinter import StringVar, ttk
from PIL import Image, ImageTk
from widgets.insert_icon_btn import InsertIconBtn as IB

import consts as c
from models.data_classes import SelectedInsertBtn, EntryVariableMap
from dataclasses import fields

class Toolbar(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager

        self.grid(column=0, row=0, sticky=tk.N)
        self.insert_icon_btns_refs = {}
        self.selected_insert_btn = SelectedInsertBtn(c.InsertTypeEnum.NONE, "")

        save_pdf_btn = ttk.Button(self, text="save pdf", command=self.save_pdf_btn_clicked)
        save_pdf_btn.grid(column=0, row=0, pady=5)

        select_pdf_btn = ttk.Button(self, text="open pdf", command=self.select_pdf_btn_clicked)
        select_pdf_btn.grid(column=0, row=1, pady=5)

        self.new_icon_btn = ttk.Button(self, text="add icon", command=self.new_icon_btn_clicked)
        self.new_icon_btn.grid(column=0, row=2, pady=5)

        ttk.Label(self, text="x").grid(column=0, row=3, sticky=tk.W)
        self.canvas_x = StringVar()
        self.canvas_x_entry = ttk.Entry(self, width=7, textvariable=self.canvas_x)
        self.canvas_x_entry.grid(column=1, row=3)
        self.canvas_x_entry.bind("<Return>", self.on_change_x)

        ttk.Label(self, text="y").grid(column=0, row=4, sticky=tk.W)
        self.canvas_y = StringVar()
        self.canvas_y_entry = ttk.Entry(self, width=7, textvariable=self.canvas_y)
        self.canvas_y_entry.grid(column=1, row=4)
        self.canvas_y_entry.bind("<Return>", self.on_change_y)

        ttk.Label(self, text="width").grid(column=0, row=5, sticky=tk.W)
        self.width = StringVar()
        self.width_entry = ttk.Entry(self, width=7, textvariable=self.width)
        self.width_entry.grid(column=1, row=5)
        self.width_entry.bind("<Return>", self.on_change_width)

        ttk.Label(self, text="height").grid(column=0, row=6, sticky=tk.W)
        self.height = StringVar()
        self.height_entry = ttk.Entry(self, width=7, textvariable=self.height)
        self.height_entry.grid(column=1, row=6)
        self.height_entry.bind("<Return>", self.on_change_height)

        ttk.Label(self, text="font").grid(column=0, row=7, sticky=tk.W)
        self.font = StringVar()
        self.font_entry = ttk.Entry(self, width=7, textvariable=self.font)
        self.font_entry.grid(column=1, row=7)
        self.font_entry.bind("<Return>", self.on_change_font)

        ttk.Label(self, text="size").grid(column=0, row=8, sticky=tk.W)
        self.text_size = StringVar()
        self.text_size_entry = ttk.Entry(self, width=7, textvariable=self.text_size)
        self.text_size_entry.grid(column=1, row=8)
        self.text_size_entry.bind("<Return>", self.on_change_text_size)

        insert_txt_btn = ttk.Button(self, text="add text", command=self.insert_text_btn_clicked)
        insert_txt_btn.grid(column=0, row=9, pady=5)

        self.outer_btns_container = ttk.Frame(self)
        self.outer_btns_container.grid(column=0, row=10, columnspan=2)
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

        self.last_icon_btn_row_index = 0

        self.toolbar_metadata_map = {
            "canvas_x": EntryVariableMap(self.canvas_x, self.canvas_x_entry),
            "canvas_y": EntryVariableMap(self.canvas_y, self.canvas_y_entry),
            "width": EntryVariableMap(self.width, self.width_entry),
            "height": EntryVariableMap(self.height, self.height_entry),
            "font": EntryVariableMap(self.font, self.font_entry),
            "size": EntryVariableMap(self.text_size, self.text_size_entry)
        }
        self.reset_entries()

    def on_mousewheel(self, event):
        self.btns_canvas_container.yview_scroll(-event.delta // 120, "units")

    def select_pdf_btn_clicked(self):
        self.manager.select_pdf_from_device()

    def new_icon_btn_clicked(self):
        file_path = self.manager.load_icon_btn()
        if file_path in self.insert_icon_btns_refs.keys():
            return
        
        img = Image.open(file_path)
        img = img.resize((c.DEFAULT_ICON_WIDTH, c.DEFAULT_ICON_HEIGHT))
        tk_img = ImageTk.PhotoImage(img)
            
        new_btn = IB(self.inner_btns_container, tk_img, file_path, self.last_icon_btn_row_index, self)
        new_btn.bind("<MouseWheel>", self.on_mousewheel)
        for child in new_btn.winfo_children():
            child.bind("<MouseWheel>", self.on_mousewheel)

        self.insert_icon_btns_refs[file_path] = new_btn
        self.last_icon_btn_row_index += 1

    def toggle_selected_insert_btn(self, insert_type, content):
        if (self.selected_insert_btn.content == content and insert_type == c.InsertTypeEnum.ICON) or self.selected_insert_btn.insert_type == c.InsertTypeEnum.ENTRY == insert_type:
            self.selected_insert_btn.insert_type = c.InsertTypeEnum.NONE
            self.selected_insert_btn.content = ""
        else:
            self.selected_insert_btn.insert_type = insert_type
            self.selected_insert_btn.content = content

    def save_pdf_btn_clicked(self):
        self.manager.save_pdf()

    def on_change_x(self, event):
        self.manager.change_icon_pos("canvas_x", float(self.canvas_x.get()))

    def on_change_y(self, event):
        self.manager.change_icon_pos("canvas_y", float(self.canvas_y.get()))

    def on_change_width(self, event):
        self.manager.change_icon_size("width", int(self.width.get()))

    def on_change_height(self, event):
        self.manager.change_icon_size("height", int(self.height.get()))

    def on_change_font(self, event):
        pass

    def on_change_text_size(self, event):
        pass

    def insert_text_btn_clicked(self):
        self.toggle_selected_insert_btn(c.InsertTypeEnum.ENTRY, "")
    
    def populate_entries(self, metadata):
        element_properties = [prop.name for prop in fields(metadata)]

        for property in self.toolbar_metadata_map.keys():
            var_entry_pair = self.toolbar_metadata_map[property]
            var = var_entry_pair.string_var
            entry = var_entry_pair.entry
            
            if property in element_properties:
                var.set(getattr(metadata, property))
                entry.configure(state="normal")
            else:
                var.set("")
                entry.configure(state="readonly")

    def reset_entries(self):
        for property in self.toolbar_metadata_map.keys():
            var_entry_pair = self.toolbar_metadata_map[property]
            var = var_entry_pair.string_var
            entry = var_entry_pair.entry
            
            var.set("")
            entry.configure(state="readonly")

    def delete_insert_icon_btn_ref(self, file_path):
        if self.selected_insert_btn.content == file_path:
            self.selected_insert_btn.insert_type = c.InsertTypeEnum.NONE
            self.selected_insert_btn.content = ""
        self.insert_icon_btns_refs.pop(file_path)