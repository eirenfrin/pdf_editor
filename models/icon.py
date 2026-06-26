
from models.data_classes import IconMetadata
import consts as c

class Icon():
    def __init__(self, file_path, tk_img, x, y, page_number):
        self.id = None
        self.tk_img = tk_img
        self.file_path = file_path
        self.width = c.DEFAULT_ICON_WIDTH
        self.height = c.DEFAULT_ICON_HEIGHT
        self.page_number = page_number
        self.canvas_x = x
        self.canvas_y = y

    def set_id(self, icon_id):
        self.id = icon_id

    def get_size_pos(self):
        return IconMetadata(self.width, self.height, self.canvas_x, self.canvas_y)
    
    def update_attr(self, prop, new_value):
        setattr(self, prop, new_value)
    

    
    
