import tkinter as tk
from tkinter import StringVar, ttk
from events.observer import Observer
import consts as c


class PdfViewer(ttk.Frame):
    def __init__(self, parent, manager, pdf_params):
        super().__init__(parent)
        self.manager = manager

        self.grid(column=1, row=0, padx=20)

        self.selected_icon = {
            "insert_type": "",
            "icon_id": None,
            "border_id": None
        }

        self.edited_text_id = ""
        
        self.update_view(pdf_params)

    def update_view(self, pdf_params):
        self.viewer = tk.Canvas(self, width=pdf_params["page_width"], height=pdf_params["page_height"])
        self.viewer.grid(row=0, column=0, sticky="nsew")
 
        for page_num, top_coord in enumerate(pdf_params["pdf_pages_tops_coords"]):
            self.viewer.create_image(0, top_coord, image=pdf_params["pdf_pages"][page_num], anchor="nw")

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
        style = ttk.Style()
        style.configure(
            "Insert.TEntry",
            font=("Arial", 16)
        )

        # input_text = StringVar()
        active_entry = ttk.Entry(self.viewer, style="Insert.TEntry", font=("Arial", 16))
        active_window = self.viewer.create_window(
            x, y,
            window=active_entry,
            anchor="nw"
        )
        if self.selected_icon["insert_type"] == c.InsertType.TEXT:
            self.save_inserted_text()
        self.selected_icon["insert_type"] = c.InsertType.TEXT
        self.selected_icon["icon_id"] = active_entry
        self.selected_icon["border_id"] = active_window
        active_entry.focus_set()

        active_entry.bind("<Return>", self.save_inserted_text)

        # if enter - save/delete
        # if clicked outside - save/delete

    def reset_selected_icon(self):
        self.selected_icon["insert_type"] = ""
        self.selected_icon["icon_id"] = ""
        self.selected_icon["border_id"] = ""

    def save_inserted_text(self, event=None):
        text_data = {
            "id": None,
            "text": None,
            "x": None,
            "y": None
        }
        active_entry = self.selected_icon["icon_id"]
        text = active_entry.get().strip()
        text_data["text"] = text

        if self.edited_text_id:
            self.save_edit_text_content(text_data)

        text_id = None
        if text:
            x, y = self.viewer.coords(self.selected_icon["border_id"])
            text_id = self.viewer.create_text(
                x, y,
                text=text,
                anchor="nw",
                font=("Arial", 16)
            )
            text_data["id"] = text_id
            text_data["x"] = x
            text_data["y"] = y

            self.viewer.tag_bind(
                text_id,
                "<Button-1>",
                self.on_text_click
            )

        self.viewer.delete(self.selected_icon["border_id"])
        self.reset_selected_icon()
        return text_data

    def save_edit_text_content(self, text_data):
        self.viewer.itemconfigure(
                self.edited_text_id,
                text=text_data["text"],
                state="normal"
        )
        self.edited_text_id = ""

    def on_text_click(self, event):
        text_id = self.viewer.find_withtag("current")[0]
        if self.edited_text_id:
            return
        self.edited_text_id = text_id
        x, y = self.viewer.coords(text_id)

        active_entry = ttk.Entry(self.viewer, font=("Arial", 16))
        active_window = self.viewer.create_window(
            x, y,
            window=active_entry,
            anchor="nw"
        )
        active_entry.focus_set()
        active_entry.bind("<Return>", self.save_inserted_text)

        # self.selected_icon["insert_type"] = c.InsertType.TEXT
        # self.selected_icon["icon_id"] = active_entry
        # self.selected_icon["border_id"] = active_window

        old_text = self.viewer.itemcget(text_id, "text")
        active_entry.insert(0, old_text)
        self.viewer.itemconfigure(text_id, state="hidden")
    
    def change_icon_pos(self, new_x, new_y):
        self.viewer.coords(self.selected_icon["icon_id"], new_x, new_y)
        x1, y1, x2, y2 = self.viewer.bbox(self.selected_icon["icon_id"])
        self.viewer.coords(self.selected_icon["border_id"], x1, y1, x2, y2)

    def change_icon_size(self, new_tk_img):
        self.viewer.itemconfig(self.selected_icon["icon_id"], image=new_tk_img)
        x1, y1, x2, y2 = self.viewer.bbox(self.selected_icon["icon_id"])

        border_id = self.viewer.create_rectangle(
            x1, y1, x2, y2,
            outline="blue",
            width=4
        )
        
        self.viewer.tag_lower(border_id, self.selected_icon["icon_id"])
        self.viewer.delete(self.selected_icon["border_id"])
        self.selected_icon["border_id"] = border_id

    
    def on_icon_click(self, event):
        icon_id = self.viewer.find_withtag("current")[0]
        self.select_icon(icon_id)

    def select_icon(self, icon_id):
        if self.selected_icon["icon_id"] != icon_id:
            if self.selected_icon["border_id"]:
                self.viewer.delete(self.selected_icon["border_id"])

            x1, y1, x2, y2 = self.viewer.bbox(icon_id)

            border_id = self.viewer.create_rectangle(
                x1, y1, x2, y2,
                outline="blue",
                width=4
            )
            self.viewer.tag_lower(border_id, icon_id)
            self.selected_icon["icon_id"] = icon_id
            self.selected_icon["border_id"] = border_id

            self.manager.load_selected_icon_info(icon_id)
            self.viewer.focus_set()
        else:
            self.viewer.delete(self.selected_icon["border_id"])
            self.selected_icon["icon_id"] = None
            self.selected_icon["border_id"] = None
            self.manager.empty_icon_info()
    
    def delete_selected(self, event):
        self.viewer.delete(self.selected_icon["icon_id"])
        self.viewer.delete(self.selected_icon["border_id"])
        self.manager.delete_selected_icon(self.selected_icon["icon_id"])

    def delete_icon(self, icon_id):
        self.viewer.delete(icon_id)

