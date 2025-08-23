import os
from textnode_helpers import (
    extract_title,
    markdown_to_html_node
)
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