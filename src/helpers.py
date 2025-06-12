import re
from enum import Enum
from texnode import TextNode, TextType
from htmlnode import HtmlNode
from parentnode import ParentNode
from leafnode import LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\]]*)\]\(([^)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # Only process TextType.NORMAL nodes for images
        if old_node.type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)

        # If no images found, add the original node as is
        if not images:
            new_nodes.append(old_node)
            continue

        current_text = text
        for alt_text, url in images:
            # Construct the full markdown image string to use as a delimiter
            image_markdown = f"![{alt_text}]({url})"
            
            # Split the current_text by the image markdown, only once
            parts = current_text.split(image_markdown, 1)

            # Check for invalid parsing, should always have two parts if image was found
            if len(parts) != 2:
                raise ValueError("Invalid markdown image syntax or unexpected split behavior.")

            # Add the text before the image
            if parts[0]: # Avoid adding empty TextNodes
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            
            # Add the image node itself
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Update current_text to be the remainder after the current image
            current_text = parts[1]
        
        # Add any remaining text after the last image
        if current_text: # Avoid adding empty TextNodes
            new_nodes.append(TextNode(current_text, TextType.NORMAL))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # Only process TextType.NORMAL nodes for links
        if old_node.type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)

        # If no links found, add the original node as is
        if not links:
            new_nodes.append(old_node)
            continue

        current_text = text
        for link_text, url in links:
            # Construct the full markdown link string to use as a delimiter
            link_markdown = f"[{link_text}]({url})"
            
            # Split the current_text by the link markdown, only once
            parts = current_text.split(link_markdown, 1)

            # Check for invalid parsing, should always have two parts if link was found
            if len(parts) != 2:
                raise ValueError("Invalid markdown link syntax or unexpected split behavior.")

            # Add the text before the link
            if parts[0]: # Avoid adding empty TextNodes
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            
            # Add the link node itself
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            
            # Update current_text to be the remainder after the current link
            current_text = parts[1]
        
        # Add any remaining text after the last link
        if current_text: # Avoid adding empty TextNodes
            new_nodes.append(TextNode(current_text, TextType.NORMAL))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    return nodes

def markdown_to_blocks(markdown : str) -> list[str]:
    cleaned_markdown = markdown.strip()
    blocks = cleaned_markdown.split("\n\n")
    final_blocks = []

    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            final_blocks.append(stripped_block)
            
    return final_blocks

def block_to_blocktype(block: str) -> BlockType:
    lines = block.split('\n')

    if block.startswith("#") and block.lstrip("#").startswith(" ") and 1 <= len(block.split(" ")[0]) <= 6:
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    is_unordered_list = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    is_ordered_list = True
    for i, line in enumerate(lines, 1):
        expected_prefix = f"{i}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    # default to paragraph
    return BlockType.PARAGRAPH

def text_to_html_nodes(text: str) -> list[HtmlNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node.text_node_to_html_node())
    return html_nodes

def heading_block_to_html_node(block: str) -> HtmlNode:
    heading_level = len(block.split(" ")[0])
    if not (1 <= heading_level <= 6):
        raise ValueError(f"Invalid heading level. Must start with 1 to 6 hash characters: {block}")
    
    heading_text = block.lstrip("#").strip()
    children = text_to_html_nodes(heading_text)
    return ParentNode(f"h{heading_level}", children)

def code_block_to_html_node(block: str) -> HtmlNode:
    if not (block.startswith("```") and block.endswith("```")):
        raise ValueError(f"Invalid code block. Must start with '```' and end with '```': {block.strip()}")
    
    code_content = block[3:-3].strip()
    code_leaf = LeafNode("code", code_content)
    
    return ParentNode("pre", [code_leaf])

def quote_block_to_html_node(block: str) -> HtmlNode:
    lines = block.split("\n")
    clean_lines = []
    
    for line in lines:
        if not line.startswith(">"):
            raise ValueError(f"Invalid quote block. All lines must begin with a '>' character: {line.strip()}")
        
        clean_lines.append(line[1:].strip())
    
    inner_text = "\n".join(clean_lines)
    children = text_to_html_nodes(inner_text)
    
    return ParentNode("blockquote", children)

def ul_block_to_html_node(block: str) -> HtmlNode:
    lines = block.split("\n")
    list_items = []

    for line in lines:
        if not line.startswith("- "):
            raise ValueError(f"Invalid unordered list block. All lines must begin with a '- ' character: {line.strip()}")
        
        inner_text = line[2:].strip()
        li_children = text_to_html_nodes(inner_text)
        list_items.append(ParentNode("li", li_children))
    
    return ParentNode("ul", list_items)

def ol_block_to_html_node(block: str) -> HtmlNode:
    lines = block.split("\n")
    list_items = []

    for i, line in enumerate(lines, 1):
        expected_prefix = f"{i}. "
        if not line.startswith(expected_prefix):
            raise ValueError(f"Invalid ordered list block. All lines must begin with a number followed by a '.': {line.strip()}")
        
        inner_text = line[len(expected_prefix):].strip()
        li_children = text_to_html_nodes(inner_text)
        list_items.append(ParentNode("li", li_children))
    
    return ParentNode("ol", list_items)

def paragraph_block_to_html_node(block: str) -> HtmlNode:
    inner_text = block.replace("\n", " ").strip()
    children = text_to_html_nodes(inner_text)
    return ParentNode("p", children)

def markdown_to_html_node(markdown: str) -> HtmlNode:
    blocks = markdown_to_blocks(markdown)
    children_nodes = []

    for block in blocks:
        block_type = block_to_blocktype(block)
        
        if block_type == BlockType.HEADING:
            children_nodes.append(heading_block_to_html_node(block))
        elif block_type == BlockType.CODE:
            children_nodes.append(code_block_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children_nodes.append(quote_block_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children_nodes.append(ul_block_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children_nodes.append(ol_block_to_html_node(block))
        elif block_type == BlockType.PARAGRAPH:
            children_nodes.append(paragraph_block_to_html_node(block))
        else:
            raise ValueError(f"Invalid block type: {block_type}")
    
    return ParentNode("div", children_nodes)