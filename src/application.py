import os
import shutil
import textwrap
from helpers import markdown_to_html_node

def copy_directory_recursive(src_path: str, dest_path: str):
    print(f"Cleaning and copying from {src_path} to {dest_path}")

    if os.path.exists(dest_path):
        print(f"Removing contents from {dest_path}")
        shutil.rmtree(dest_path)
        print(f"{dest_path} is now empty")

    # if dest_path doesn't exist
    print(f"Creating directory {dest_path}...")
    os.makedirs(dest_path, exist_ok=True)
    print(f"Directory {dest_path} created")

    for item in os.listdir(src_path):
        src_item_path = os.path.join(src_path, item)
        dest_item_path = os.path.join(dest_path, item)

        if os.path.isfile(src_item_path):
            print(f"Copying {src_item_path} to {dest_item_path}")
            shutil.copy2(src_item_path, dest_item_path)
        elif os.path.isdir(src_item_path):
            print(f"Entering subdirectory {src_item_path}")
            copy_directory_recursive(src_item_path, dest_item_path)
        else:
            print(f"Unknown file type: {src_item_path}. Skipping...") 
    
    print(f"Finished copying from {src_path} to {dest_path}")

def extract_title(markdown: str) -> str:
    header = markdown.strip().split("\n")[0].lstrip("#").strip()
    
    if not header:
        raise ValueError("No title found in Markdown")
    
    return header

def generate_page(from_path: str, template_path: str, output_path: str):
    markdown = ""
    template = ""

    print(f"Generating page from {from_path} to {output_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read().strip()

    cleaned_markdown = textwrap.dedent(markdown).strip()
    print(f"Markdown: {cleaned_markdown}")

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(cleaned_markdown).to_html()
    title = extract_title(cleaned_markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(page)

    print(f"Page generated at {output_path}")