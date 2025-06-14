import os
from application import *

def main():
    static_dir = "static"
    public_dir = "public"
    content_dir = "content"
    template_file = "template.html"

    if not os.path.exists(static_dir):
        print(f"Error, source directory does not exist: {static_dir}")
        return

    if not os.path.exists(content_dir):
        print(f"Error, content directory does not exist: {content_dir}")
        return
    
    copy_directory_recursive(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_file, public_dir)

if __name__ == "__main__":
    main()