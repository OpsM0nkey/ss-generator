from textnode import TextNode, TextType
from copy_static_content import copy_static_content
from generate_page import generate_page

def main():
    
    copy_static_content("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()