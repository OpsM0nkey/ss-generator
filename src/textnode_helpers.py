import re

from textnode import TextNode, TextType

def is_textnode(input_node):
    return isinstance(input_node, TextNode)

def markdown_splitter(text, delimiter, expected_type: TextType):
    text_node_list = []
    split_list = text.split(delimiter)
    # original algo was faulty. Every second (i.e even) element in the list is going to be a text block no matter how you break it.
    # below is a copied correction from the course.
    for item in range(len(split_list)):
        if split_list[item] == "":
            continue
        if item % 2 == 0:
            text_node_list.append(TextNode(split_list[item], TextType.TEXT))
        else:
            text_node_list.append(TextNode(split_list[item], expected_type)) 
    
    return text_node_list


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    nodes_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes_list.append(node)
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise SyntaxError(f"Node text is missing a closing delimiter '{delimiter}'. Check your input string.")
            
            nodes_list.extend(markdown_splitter(node.text, delimiter, text_type))
    
    return nodes_list
            
def extract_markdown_images(text) -> tuple:
    if len(text) == 0:
        raise Exception("Input text string cannot be null or emtpy")

    image_data = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)    
    return image_data

def extract_markdown_links(text):
   if len(text) == 0:
        raise Exception("Input text string cannot be null or emtpy")

   link_data = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return link_data