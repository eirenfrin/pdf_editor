import consts as c
from models.data_classes import TextMetadata

class Text():
    def __init__(self, text_id, content, page_number, x, y):
        self.id = text_id
        self.content = content
        self.font = c.DEFAULT_TEXT_FONT
        self.size = c.DEFAULT_TEXT_SIZE
        self.page_number = page_number
        self.canvas_x = x
        self.canvas_y = y

    def get_style_pos(self):
        return TextMetadata(self.font, self.size, self.canvas_x, self.canvas_y)
    
    def update_attr(self, prop, new_value):
        setattr(self, prop, new_value)
