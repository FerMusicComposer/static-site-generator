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