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
            
def extract_markdown_images(text: str) -> tuple:
    if len(text) == 0:
        raise Exception("Input text string cannot be null or emtpy")

    image_data = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)    
    return image_data

def extract_markdown_links(text: str):
   if len(text) == 0:
        raise Exception("Input text string cannot be null or emtpy")

   link_data = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return link_data

def split_nodes_image(old_nodes: list) -> list:
    nodes_list = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        # if there are no images, append the full text string and return
        if len(images) == 0:
            nodes_list.append(node)
            continue
        
        # set temp variable to keep track of remaining text
        remaining_text = node.text
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            # make sure left side of split is not None or empty
            if sections[0].strip():
                nodes_list.append(TextNode(sections[0], TextType.TEXT))

            # then, append the image data
            nodes_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
            remaining_text = sections[1]

        # if there is any text left over, append that
        if remaining_text and not remaining_text.isspace():
            nodes_list.append(TextNode(remaining_text, TextType.TEXT))
    return nodes_list


def split_nodes_link(old_nodes: list) -> list:
    nodes_list = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)

        # if there are no links, append the full text string and return
        if len(links) == 0:
            nodes_list.append(node)
            continue
        
        # set temp variable to keep track of remaining text
        remaining_text = node.text
        for link in links:
            link_text = link[0]
            link_url = link[1]
            sections = remaining_text.split(f"[{link_text}]({link_url})", 1)
            # make sure left side of split is not None or empty
            if sections[0].strip():
                nodes_list.append(TextNode(sections[0], TextType.TEXT))

            # then, append the link data
            nodes_list.append(TextNode(link_text, TextType.LINK, link_url))
            remaining_text = sections[1]

        # if there is any text left over, append that
        if remaining_text and not remaining_text.isspace():
            nodes_list.append(TextNode(remaining_text, TextType.TEXT))
    return nodes_list

def text_to_textnodes(text: str) -> list:
    nodes_list = []
    # convert text to textnode
    starting_text = TextNode(text, TextType.TEXT)

    # get bold
    nodes_list = split_nodes_delimiter([starting_text], "**", TextType.BOLD)
    # get code
    nodes_list = split_nodes_delimiter(nodes_list, "`", TextType.CODE)
    # get italic
    nodes_list = split_nodes_delimiter(nodes_list, "_", TextType.ITALIC)
    # split any images
    nodes_list = split_nodes_image(nodes_list)
    # get links
    nodes_list = split_nodes_link(nodes_list)

    return nodes_list

def markdown_to_blocks(markdown: str) -> list:

    # split the markdown by the newline
    block_list = markdown.split(f"\n\n")

    # list that we'll return out
    final_block_list = []
    for block in block_list:
        if block and not block.isspace():
            final_block_list.append(block.strip())

    return final_block_list

