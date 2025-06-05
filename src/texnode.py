from enum import Enum

class TextType(Enum):
    NORMAL = "Normal"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode:
    def __init__(self, text, type, url=None):
        self.text = text
        self.type = type
        self.url = url
    
    def __eq__(self, value):
        if not isinstance(value, self.__class__):
            return False
        return self.text == value.text and self.type == value.type and self.url == value.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.type.value}, {self.url})"