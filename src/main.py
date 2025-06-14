import os
import sys
from application import *

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    if basepath and not basepath.endswith('/'):
        basepath += '/'
    
    static_dir = "static"
    output_dir = "docs"
    content_dir = "content"
    template_file = "template.html"

    print(f"Starting page generation with basepath: {basepath}")

    if not os.path.exists(static_dir):
        print(f"Error, source directory does not exist: {static_dir}")
        return

    if not os.path.exists(content_dir):
        print(f"Error, content directory does not exist: {content_dir}")
        return
    
    copy_directory_recursive(static_dir, output_dir)
    generate_pages_recursive(basepath, content_dir, template_file, output_dir)

    print("Page generation complete")

if __name__ == "__main__":
    main()