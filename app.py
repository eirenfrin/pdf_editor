import tkinter as tk
from edit_manager import EditManager as Manager

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        print(self.tk.call("tk", "scaling"))

        self.edit_manager = Manager(self)
