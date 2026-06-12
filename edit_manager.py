from events.observer import Observer
import consts as c
import os
from PIL import Image, ImageTk, ImageOps

class EditManager(Observer):
    def __init__(self, model, toolbar):
        self.model = model
        self.toolbar = toolbar
        self.added_icons_storage = {}

    def calculate_icon_canvas_params(self):
        if self.toolbar.selected_icon[0]:
            path = os.path.join(c.input_folder, self.toolbar.selected_icon[0])
            img = Image.open(path)
            img = img.resize((60, 60))
            # img = ImageOps.exif_transpose(img)
            img.save(os.path.join("temp", self.toolbar.selected_icon[0]))
            tk_img = ImageTk.PhotoImage(img)

            self.model.store_inserted_image_canvas_coords(self.toolbar.selected_icon[0], tk_img)

    def update(self, event, data):
        address, msg = event.split(":")
        if address == "manager":
            if msg == "add_photo":
                self.calculate_icon_canvas_params()