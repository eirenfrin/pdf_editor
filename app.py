import tkinter as tk
from edit_manager import EditManager as Manager
import consts as c

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        c.tk_scale = self.tk.call("tk", "scaling")
        self.edit_manager = Manager(self)
