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


# icon
DEFAULT_ICON_WIDTH = 60
DEFAULT_ICON_HEIGHT = 60

# text
DEFAULT_TEXT_SIZE = 16
DEFAULT_TEXT_FONT = "Arial"

# pdf
DEFAULT_OUTPUT_FILENAME = "edited.pdf"

tk_scale = None


