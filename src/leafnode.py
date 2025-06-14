from htmlnode import HtmlNode

class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("Leaf nodes must have a value")
        
        super().__init__(tag, value, None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        if not self.tag:
            return self.value

        return f"<{self.tag}{' ' + self.props_to_html() if self.props else ''}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"