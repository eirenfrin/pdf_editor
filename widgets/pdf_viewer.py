import tkinter as tk
from tkinter import StringVar, ttk
from events.observer import Observer
import consts as c
from models.data_classes import SelectedCanvasElement, TextSnapshot


class PdfViewer(ttk.Frame):
    def __init__(self, parent, manager, pdf_params):
        super().__init__(parent)
        self.manager = manager

        self.grid(column=1, row=0, padx=20)

        self.selected_element = SelectedCanvasElement(c.InsertTypeEnum.NONE, None, None)
        self.new_text_in_progress = False
        
        self.display_pdf(pdf_params)

    def display_pdf(self, pdf_params):
        self.viewer = tk.Canvas(self, width=pdf_params.page_width, height=pdf_params.page_height)
        self.viewer.grid(row=0, column=0, sticky="nsew")
 
        for page_num, top_coord in enumerate(pdf_params.pdf_pages_tops_coords):
            self.viewer.create_image(0, top_coord, image=pdf_params.pdf_pages_tk_imgs[page_num], anchor="nw")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.viewer.yview)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        
        self.viewer.bind("<MouseWheel>", self.on_mousewheel)
        self.viewer.configure(yscrollcommand=self.scrollbar.set, scrollregion=self.viewer.bbox("all"))
        self.viewer.bind("<Button-1>", self.get_mouse_coords)
        self.viewer.bind("<Delete>", self.delete_selected)
        self.viewer.bind("<BackSpace>", self.delete_selected)

    def on_mousewheel(self, event):
        self.viewer.yview_scroll(-event.delta // 120, "units")

    def get_mouse_coords(self, event):
        x = self.viewer.canvasx(event.x)
        y = self.viewer.canvasy(event.y)
        self.manager.canvas_click(x, y)
        
    def insert_icon(self, x, y, tk_img):
        icon_id = self.viewer.create_image(x, y, image=tk_img, anchor=tk.NW)
        self.viewer.tag_bind(icon_id, "<Button-1>", self.on_icon_click)

        return icon_id
    
    def insert_text_entry(self, x, y):
        self.unselect_element()
        self.new_text_in_progress = True
        style = ttk.Style()
        style.configure(
            "Insert.TEntry",
            font=("Arial", 16)
        )

        active_entry = ttk.Entry(self.viewer, style="Insert.TEntry", font=("Arial", 16))
        active_window = self.viewer.create_window(
            x, y,
            window=active_entry,
            anchor="sw"
        )

        self.selected_element.insert_type = c.InsertTypeEnum.ENTRY
        self.selected_element.element_ref = active_entry
        self.selected_element.border_ref = active_window
        active_entry.focus_set()

        active_entry.bind("<Return>", self.process_text_entry)

    def process_text_entry(self, event):
        text_data = self.manager.process_text_entry(c.ClickedTypeEnum.ENTER)
        self.select_element(text_data.id, c.InsertTypeEnum.ENTRY)

    def reset_selected_icon(self):
        self.selected_element = SelectedCanvasElement(c.InsertTypeEnum, None, None)

    def save_inserted_text(self, event=None):
        text_data = TextSnapshot(None, None, None, None)
        active_entry = self.selected_element.element_ref
        text = active_entry.get().strip()

        if not text:
            self.unselect_element()
            self.reset_selected_icon()
            self.new_text_in_progress = False
            return text_data

        x, y = self.viewer.coords(self.selected_element.border_ref)
        self.unselect_element() # delete entry

        text_id = self.viewer.create_text(
            x, y,
            text=text,
            anchor="sw",
            font=("Arial", 16)
        )
        text_snapshot = TextSnapshot(text_id, text, x, y)

        self.viewer.tag_bind(
            text_id,
            "<Button-1>",
            self.on_text_click
        )

        self.new_text_in_progress = False
        return text_snapshot
    
    def change_icon_pos(self, new_x, new_y):
        self.viewer.coords(self.selected_element.element_ref, new_x, new_y)
        x1, y1, x2, y2 = self.viewer.bbox(self.selected_element.element_ref)
        self.viewer.coords(self.selected_element.border_ref, x1, y1, x2, y2)

    def change_icon_size(self, new_tk_img):
        self.viewer.itemconfig(self.selected_element.element_ref, image=new_tk_img)
        x1, y1, x2, y2 = self.viewer.bbox(self.selected_element.element_ref)

        border_id = self.viewer.create_rectangle(
            x1, y1, x2, y2,
            outline="blue",
            width=4
        )
        
        self.viewer.tag_lower(border_id, self.selected_element.element_ref)
        self.viewer.delete(self.selected_element.border_ref)
        self.selected_element.border_ref = border_id
    
    def on_text_click(self, event):
        if self.new_text_in_progress:
            self.manager.process_text_entry(c.ClickedTypeEnum.ELEMENT)
        text_id = self.viewer.find_withtag("current")[0]
        self.select_element(text_id, c.InsertTypeEnum.TEXT)

    def on_icon_click(self, event):
        if self.new_text_in_progress:
            self.manager.process_text_entry(c.ClickedTypeEnum.ELEMENT)
        icon_id = self.viewer.find_withtag("current")[0]
        self.select_element(icon_id, c.InsertTypeEnum.ICON)

    def unselect_element(self):
        self.viewer.delete(self.selected_element.border_ref)
        self.reset_selected_icon()

    def select_element(self, id, insert_type):
        if self.selected_element.element_ref != id:
            if self.selected_element.border_ref:
                self.viewer.delete(self.selected_element.border_ref)

            x1, y1, x2, y2 = self.viewer.bbox(id)

            border_id = self.viewer.create_rectangle(
                x1, y1, x2, y2,
                outline="blue",
                width=4
            )
            self.viewer.tag_lower(border_id, id)
            self.selected_element.element_ref = id
            self.selected_element.border_ref = border_id
            self.selected_element.insert_type = insert_type

            if self.selected_element.insert_type == c.InsertTypeEnum.ICON:
                self.manager.load_selected_icon_info(id)
            elif self.selected_element.insert_type == c.InsertTypeEnum.TEXT:
                self.manager.load_selected_text_info(id)
            self.viewer.focus_set()
        else:
            self.unselect_element()
            self.manager.empty_element_info()
    
    def delete_selected(self, event):
        self.viewer.delete(self.selected_element.element_ref)
        self.unselect_element()
        self.manager.delete_element_model()


