import re
from texnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        splits = old_node.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: closing delimiter '{delimiter}' not found in '{old_node.text}'")

        for i in range(len(splits)):
            if splits[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(splits[i], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(splits[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)