import os
import shutil

def copy_static_content(src: str, dest: str) -> None:
    
    # first, make sure the source directory exists
    if not os.path.exists(src):
        raise ValueError(f"Source path [{src}] not found")
    
    # get absolute paths for each
    src_full = os.path.abspath(src)
    dest_full = os.path.abspath(dest)
    
    # first delete dest
    if os.path.exists(dest_full):
        shutil.rmtree(dest_full)
    
    # then re-create it
    os.mkdir(dest_full)

    # get contents of source
    for item in os.listdir(src_full):
        src_item_path = os.path.join(src_full, item)
        dest_item_path = os.path.join(dest_full, item)
        if os.path.isfile(src_item_path):
            shutil.copy(src_item_path, dest_item_path)
        else:
            copy_static_content(src_item_path, dest_item_path)
    

    