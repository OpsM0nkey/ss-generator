import os
from textnode_helpers import (
    extract_title,
    markdown_to_html_node
)
from pathlib import Path

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, 'r') as file:
            from_content = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{from_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
    except FileNotFoundError:
        print(f"Error: Template file path '{template_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # convert to HTMLNode and generate html content
    html_content = (markdown_to_html_node(from_content)).to_html()
    content_title = extract_title(from_content)

    page_html = (template_content.replace("{{ Content }}", html_content)).replace("{{ Title }}", content_title)

    # check if the destination directories exist, if not create them
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w') as file:
        file.write(page_html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    # first, make sure the source directory exists
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Source path [{dir_path_content}] not found")

    # get absolute paths for each
    content_full = os.path.abspath(dir_path_content)
    dest_full = os.path.abspath(dest_dir_path)

    for item in os.listdir(content_full):
        src_item_path = os.path.join(content_full, item)
        dest_item_path = os.path.join(dest_full, item)

        if not os.path.isfile(src_item_path):
            generate_pages_recursive(src_item_path, template_path, dest_item_path)
        
        # use generate_page to generate the html and copy to the target
        if Path(src_item_path).suffix.lower() == ".md":
            generate_page(src_item_path, template_path, dest_item_path.replace(".md", ".html"))
