import tkinter as tk
from tkinter import ttk
from events.observer import Observer


class PdfViewer(ttk.Frame):
    def __init__(self, parent, manager, pdf_params):
        super().__init__(parent)
        self.manager = manager

        self.grid(column=1, row=0, padx=20)
        self.update_view(pdf_params)

        self.selected_icon = (None, None)

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

    def on_mousewheel(self, event):
        self.viewer.yview_scroll(-event.delta // 120, "units")

    def get_mouse_coords(self, event):
        x = self.viewer.canvasx(event.x)
        y = self.viewer.canvasy(event.y)
        
        self.manager.canvas_click_callback(x, y)
        
    def insert_icon(self, x, y, tk_img):
        icon_id = self.viewer.create_image(x, y, image=tk_img, anchor=tk.NW)
        self.viewer.tag_bind(icon_id, "<Button-1>", self.on_icon_click)

        return icon_id
    
    def change_icon_pos(self, new_x, new_y):
        self.viewer.coords(self.selected_icon[0], new_x, new_y)
        x1, y1, x2, y2 = self.viewer.bbox(self.selected_icon[0])
        self.viewer.coords(self.selected_icon[1], x1, y1, x2, y2)

    def change_icon_size(self, new_tk_img):
        self.viewer.itemconfig(self.selected_icon[0], image=new_tk_img)
        x1, y1, x2, y2 = self.viewer.bbox(self.selected_icon[0])

        border_id = self.viewer.create_rectangle(
            x1, y1, x2, y2,
            outline="blue",
            width=4
        )
        
        self.viewer.tag_lower(border_id, self.selected_icon[0])
        self.viewer.delete(self.selected_icon[1])
        self.selected_icon = (self.selected_icon[0], border_id)

    
    def on_icon_click(self, event):
        icon_id = self.viewer.find_withtag("current")[0]
        self.select_icon(icon_id)

    def select_icon(self, icon_id):

        if self.selected_icon[0] != icon_id:
            if self.selected_icon[1]:
                self.viewer.delete(self.selected_icon[1])

            x1, y1, x2, y2 = self.viewer.bbox(icon_id)

            border_id = self.viewer.create_rectangle(
                x1, y1, x2, y2,
                outline="blue",
                width=4
            )
            self.viewer.tag_lower(border_id, icon_id)
            self.selected_icon = (icon_id, border_id)

            self.manager.load_selected_icon_info(icon_id)
        else:
            self.viewer.delete(self.selected_icon[1])
            self.selected_icon = (None, None)

    def delete_icon(self, icon_id):
        self.viewer.delete(icon_id)

