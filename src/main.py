import os
from application import *

def main():
    static_dir = "static"
    public_dir = "public"

    if not os.path.exists(static_dir):
        print(f"Error, source directory does not exist: {static_dir}")
        return

    copy_directory_recursive(static_dir, public_dir)
    generate_page("content/index.md", "template.html", f"{public_dir}/index.html")

if __name__ == "__main__":
    main()