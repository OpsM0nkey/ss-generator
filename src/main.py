import sys
from textnode import TextNode, TextType
from copy_static_content import copy_static_content
from generate_page import generate_page, generate_pages_recursive

def main():
    # check provided arguments to set the base path, if none, set to "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    print(f"Using basepath: {basepath}")
    copy_static_content("static", "docs")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(basepath=basepath, dir_path_content="content", template_path="template.html", dest_dir_path="docs")


if __name__ == "__main__":
    main()