from enum import Enum, auto

class InsertTypeEnum(Enum):
    ENTRY = auto()
    ICON = auto()
    TEXT = auto()
    NONE = auto()

class ClickedTypeEnum(Enum):
    CANVAS_INSERT = auto()
    CANVAS_EMPTY = auto()
    ELEMENT = auto()
    ENTER = auto()


output_folder = "output"
output_file = "edited.pdf"


