from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            raise TypeError(f"Comparison object must be of type TextNode. Received {type(other)}")
        
        return (
            self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url
            )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode):

    if not isinstance(text_node, TextNode):
            raise TypeError(f"Input parameter must be of type TextNode. Received {type(text_node)}")
    
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            properties = {
                "href": text_node.url
            }
            return LeafNode("a", text_node.text, properties)
        case TextType.IMAGE:
            properties = {
                "src": text_node.url,
                "alt": text_node.text
            }
            return LeafNode("img", "", properties)
        case _:
            raise ValueError(f"Input text_type [{text_node.text_type}] not supported.")