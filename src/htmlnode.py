class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        
        return ' '.join(f'{key}="{str(value)}"' for key, value in self.props.items())

    def __eq__(self, value): 
        if not isinstance(value, HtmlNode):
            return False
        return (
            self.tag == value.tag and
            self.value == value.value and
            self.children == value.children and # This needs to handle list/None
            self.props == value.props          # This needs to handle dict/None
        )
    
    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
