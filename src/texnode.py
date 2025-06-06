from enum import Enum
from leafnode import LeafNode

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
    
    def text_node_to_html_node(self):
        if self.type == TextType.NORMAL:
            return LeafNode(None, self.text, None)
        elif self.type == TextType.BOLD:
            return LeafNode("b", self.text, None)
        elif self.type == TextType.ITALIC:
            return LeafNode("i", self.text, None)
        elif self.type == TextType.CODE:
            return LeafNode("code", self.text, None)
        elif self.type == TextType.LINK:
            return LeafNode("a", self.text, {"href": self.url})
        elif self.type == TextType.IMAGE:
            return LeafNode("img", "", {"src": self.url, "alt": self.text})

    def __eq__(self, value):
        if not isinstance(value, self.__class__):
            return False
        return self.text == value.text and self.type == value.type and self.url == value.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.type.value}, {self.url})"