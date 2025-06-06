from htmlnode import HtmlNode
from leafnode import LeafNode

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent nodes must have a tag")
        
        if not self.children:
            raise ValueError("Parent nodes must have children")
        
        props_str = f" {self.props_to_html()}" if self.props is not None else ""
        html = f"<{self.tag}{props_str}>"
        for child in self.children:
            if isinstance(child, HtmlNode):
                html += child.to_html() 
            else:
                html += str(child)
        html += f"</{self.tag}>"
        return html
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
