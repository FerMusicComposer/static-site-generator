import os
import shutil

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