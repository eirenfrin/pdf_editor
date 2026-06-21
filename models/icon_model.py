
class IconModel():
    def __init__(self, img_path, tk_img, x, y, page):
        self.icon_id = 0
        self.tk_img = tk_img
        self.img_path = img_path
        self.width = 60
        self.height = 60
        self.page = page
        self.canvas_x = x
        self.canvas_y = y

    def set_id(self, icon_id):
        self.icon_id = icon_id

    def get_model_size_pos(self):
        return {
            "width": self.width,
            "height": self.height,
            "canvas_x": self.canvas_x,
            "canvas_y": self.canvas_y
        }
    
    def update_pos(self, prop, new_value):
        setattr(self, prop, new_value)

        return (self.canvas_x, self.canvas_y)
    
    def update_size(self, prop, new_value):
        setattr(self, prop, new_value)

        return (self.width, self.height)
    
    def update_tk_img(self, new_tk_img):
        self.tk_img = new_tk_img