import tkinter as tk
from tkinter import ttk
from events.observer import Observer


class PdfViewer(ttk.Frame):
    def __init__(self, parent, manager, pdf_params):
        super().__init__(parent)
        self.manager = manager

        self.grid(column=1, row=0, padx=20)

        self.viewer = tk.Canvas(self, width=pdf_params["page_width"], height=pdf_params["page_height"])
        self.viewer.grid(row=0, column=0, sticky="nsew")
 
        for page_num, top_coord in enumerate(pdf_params["pdf_pages_tops_coords"]):
            self.viewer.create_image(0, top_coord, image=pdf_params["pdf_pages"][page_num], anchor="nw")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.viewer.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.viewer.bind("<MouseWheel>", self.on_mousewheel)
        self.viewer.configure(yscrollcommand=self.scrollbar.set, scrollregion=self.viewer.bbox("all"))
        self.viewer.bind("<Button-1>", self.get_mouse_coords)

    def on_mousewheel(self, event):
        self.viewer.yview_scroll(-event.delta // 120, "units")

    def get_mouse_coords(self, event):
        x = self.viewer.canvasx(event.x)
        y = self.viewer.canvasy(event.y)
        
        self.manager.canvas_click_callback(x, y)
        
    def insert_icon(self, x, y, tk_img):
        icon_id = self.viewer.create_image(x, y, image=tk_img, anchor=tk.NW)

        return icon_id

    def delete_icon(self, icon_id):
        self.viewer.delete(icon_id)

