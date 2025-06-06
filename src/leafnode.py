from htmlnode import HtmlNode

class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        
        if not self.tag:
            return self.value

        return f"<{self.tag}{' ' + self.props_to_html() if self.props else ''}>{self.value}</{self.tag}>"
