import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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


def block_is_ordered_list(markdown: str) -> bool:
    # split the block
    md_split = markdown.split("\n")

    # if the first line doesn't start with "1. ", it's not an ordered list.
    if not md_split[0].startswith("1. "):
        return False
    
    # keep track of the counter
    line_counter = 1
    for line in md_split:
        if line.startswith(f"{line_counter}. "):
            line_counter += 1
            continue
        else:
            return False
    
    return True

def block_is_unordered_list(markdown: str) -> bool:
    # split the block and check each line starts with "- "
    md_split = markdown.split("\n")

    for line in md_split:
        if not line.startswith("- "):
            return False
    
    return True

def block_is_quote(markdown: str) -> bool:
    # split the block and check if each line starts with "> "
    md_split = markdown.split("\n")

    for line in md_split:
        if not line.startswith(">"):
            return False

    return True

def block_to_block_type(markdown: str) -> BlockType:

    # switch through the markdown block to determine the blocktype:
    # trim to remove leading and trailing whitespace
    markdown = markdown.strip()
    match markdown:
        # check the tuple for the 1-6 valid header combinations (including whitespace after "#")
        case markdown if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.HEADING
        case markdown if markdown.startswith("```") and markdown.endswith("```"):
            return BlockType.CODE
        case markdown if block_is_quote(markdown):
            return BlockType.QUOTE
        case markdown if block_is_unordered_list(markdown):
            return BlockType.UNORDERED_LIST
        case markdown if block_is_ordered_list(markdown):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH
        
def convert_newline_to_space(text: str) -> str:
    return text.replace("\n", " ")
        
def text_to_children(text: str) -> list:
    child_nodes = []
    text_nodes = text_to_textnodes(convert_newline_to_space(text))


    # for each node, convert to leafnode
    for node in text_nodes:
        child_nodes.append(text_node_to_html_node(node))
    
    return child_nodes

def get_html_heading_type(heading: str) -> str:

    # determine the heading level
    heading_level = heading.count("#")
    return f"h{heading_level}"

def clean_unordered_list_item(item: str) -> str:
    return item.lstrip("- ").strip()

def get_unordered_list_items(list_items: list) -> list:

    # each item is a leafNode, process and return a <li> element using a list comprehension
    return [
        ParentNode("li", text_to_children(clean_unordered_list_item(item)))
        for item in list_items
    ]

def clean_ordered_list_item(item: str) -> str:
    return re.sub(r"^\d+\.\s+", "", item.lstrip())

def get_ordered_list_items(list_items: list) -> list:
    return [
        ParentNode("li", text_to_children(clean_ordered_list_item(item)))
        for item in list_items
    ]

def new_html_node(block: str, block_type: BlockType) -> HTMLNode:

    match block_type:
        case BlockType.PARAGRAPH:
            child_nodes = text_to_children(block)
            html_node = ParentNode("p", child_nodes)
        
        case BlockType.HEADING:
            child_nodes = text_to_children(block)
            # determine the heading level
            heading_level = get_html_heading_type(block)
            html_node = ParentNode(heading_level, child_nodes)

        case BlockType.QUOTE:
            child_nodes = text_to_children(block)
            html_node = ParentNode("blockquote", child_nodes)

        case BlockType.UNORDERED_LIST:
            # need to split by newlines, then iteratively call text_to_children
            child_nodes = get_unordered_list_items(block.split("\n"))
            html_node = ParentNode("ul", child_nodes)
        
        case BlockType.ORDERED_LIST:
            child_nodes = get_ordered_list_items(block.split("\n"))
            html_node = ParentNode("ol", child_nodes)

        case BlockType.CODE:
            text_node = TextNode((block.strip("`")).lstrip(), TextType.CODE)
            child_nodes = text_node_to_html_node(text_node)
            html_node = ParentNode("pre", [child_nodes])

    return html_node
        
def markdown_to_html_node(markdown) -> HTMLNode:
    """
        converts a full markdown document into a single parent HTMLNode. That one parent HTMLNode should
        contain many child HTMLNode objects representing the nested elements.
    """

    # split full markdown into blocks:
    md_blocks = markdown_to_blocks(markdown)

    block_nodes = []

    for block in md_blocks: 
        block_type = block_to_block_type(block)
        html_node = new_html_node(block, block_type)
        block_nodes.append(html_node)

    return ParentNode("div", block_nodes)