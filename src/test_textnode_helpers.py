import unittest

from textnode_helpers import split_nodes_delimiter, is_textnode
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class ValidateIsTextNode(unittest.TestCase):
    def test_returns_true(self):
       node = TextNode("This is text with a `code block` word", TextType.TEXT)
       self.assertTrue(is_textnode(node))

    def test_returns_false(self):
       node = LeafNode()
       self.assertFalse(is_textnode(node))

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_splitnodes_basic_output(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(
            new_nodes[0].text,
            "This is text with a "
        )
        self.assertEqual(
            new_nodes[0].text_type,
            TextType.TEXT
        )
        self.assertEqual(
            new_nodes[1].text,
            "code block" 
        )
        self.assertEqual(
            new_nodes[1].text_type,
            TextType.CODE
        )
        self.assertEqual(
            new_nodes[2].text,
            " word" 
        )
        self.assertEqual(
            new_nodes[2].text_type,
            TextType.TEXT
        )

    def test_splitnodes_code_block_at_start(self):
        node = TextNode("`A code block` starts this text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(
            new_nodes[0].text,
            "A code block"
        )
        self.assertEqual(
            new_nodes[0].text_type,
            TextType.CODE
        )
        self.assertEqual(
            new_nodes[1].text,
            " starts this text" 
        )
        self.assertEqual(
            new_nodes[1].text_type,
            TextType.TEXT
        )
        

    def test_splitnodes_multi_node_list(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This sentence includes **bolded** text and a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(
            new_nodes[0].text_type,
            TextType.TEXT
        )
        self.assertEqual(
            new_nodes[1].text_type,
            TextType.CODE
        )
        self.assertEqual(
            new_nodes[2].text_type,
            TextType.TEXT
        )
        self.assertEqual(
            new_nodes[3].text_type,
            TextType.TEXT
        )
        self.assertEqual(
            new_nodes[4].text_type,
            TextType.CODE
        )

    def test_splitnodes_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(
            new_nodes[0].text,
            "This is text with a "
        )
        self.assertEqual(
            new_nodes[0].text_type,
            TextType.TEXT
        )
        self.assertEqual(
            new_nodes[1].text,
            "bolded" 
        )
        self.assertEqual(
            new_nodes[1].text_type,
            TextType.BOLD
        )
        self.assertEqual(
            new_nodes[2].text,
            " word" 
        )
        self.assertEqual(
            new_nodes[2].text_type,
            TextType.TEXT
        )

    def test_splitnodes_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(
            new_nodes[0].text,
            "This is text with an "
        )
        self.assertEqual(
            new_nodes[0].text_type,
            TextType.TEXT
        )
        self.assertEqual(
            new_nodes[1].text,
            "italic" 
        )
        self.assertEqual(
            new_nodes[1].text_type,
            TextType.ITALIC
        )
        self.assertEqual(
            new_nodes[2].text,
            " word" 
        )
        self.assertEqual(
            new_nodes[2].text_type,
            TextType.TEXT
        )
    
    def test_splitnodes_raises_syntax_error(self):
        node = TextNode("This is text with a *malformed markdown for italic.", TextType.TEXT)
        with self.assertRaises(SyntaxError) as cm:
            split_nodes_delimiter([node], "*", TextType.ITALIC)
        raised_exception = cm.exception
        self.assertEqual(
            raised_exception.args[0], 
            "Node text is missing a closing delimiter '*'. Check your input string."
        )

if __name__ == "__main__":
    unittest.main()