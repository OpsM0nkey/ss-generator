import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_type_compare_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        other_obj = "Just a string"
        self.assertRaises(TypeError, "Comparison object must be of type TextNode.*")

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://dummyurl.org")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2) 

    def test_default_url_is_none(self):
        node = TextNode("DummyTest", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_default_url_not_none(self):
        node = TextNode("DummyTest", TextType.TEXT, "https://dummy.org")
        self.assertIsNotNone(node.url)

    def text_text_eq(self):
        node = TextNode("Node text", TextType.TEXT)
        node2 = TextNode("Node text", TextType.TEXT)
        self.assertEqual(node,node2)

    def test_text_not_eq(self):
        node = TextNode("Node1 text", TextType.TEXT)
        node2 = TextNode("Node2 text", TextType.TEXT)
        self.assertNotEqual(node,node2)

    def text_texttype_not_eq(self):
        node = TextNode("Node text", TextType.BOLD)
        node2 = TextNode("Node text", TextType.TEXT)
        self.assertNotEqual(node,node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHMLNode(unittest.TestCase):

    def test_raises_on_non_TextNode_obj(self):
        with self.assertRaises(TypeError) as cm:
            text_node_to_html_node("NotaTextNode")
        raised_exception = cm.exception
        self.assertEqual(
            raised_exception.args[0], 
            "Input parameter must be of type TextNode. Received <class 'str'>"
        )

    def test_raises_non_supported_texttype(self):
        with self.assertRaises(AttributeError) as cm:
            text_node_to_html_node(TextNode("Normal Text", TextType.RANDOM, None))
        raised_exception = cm.exception
        self.assertEqual(
            raised_exception.args[0], 
            "type object 'TextType' has no attribute 'RANDOM'"
        )

    def test_raises_ValueError_non_supported_texttype(self):
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(TextNode("Normal Text", "Squiggly", None))
        raised_exception = cm.exception
        self.assertEqual(
            raised_exception.args[0], 
            "Input text_type [Squiggly] not supported."
        )

    def test_textnode_normal_text(self):
        node = TextNode("Normal Text", TextType.TEXT, None) 
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(
            leaf_node.tag,
            None
        )
        self.assertEqual(
            leaf_node.value,
            "Normal Text"
        )
        self.assertEqual(
            leaf_node.props,
            None
        )

    def test_textnode_bold_text(self):
        node = TextNode("Bold Text", TextType.BOLD, None) 
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(
            leaf_node.tag,
            "b"
        )
        self.assertEqual(
            leaf_node.value,
            "Bold Text"
        )
        self.assertEqual(
            leaf_node.props,
            None
        )

    def test_textnode_italic_text(self):
        node = TextNode("Italic Text", TextType.ITALIC, None) 
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(
            leaf_node.tag,
            "i"
        )
        self.assertEqual(
            leaf_node.value,
            "Italic Text"
        )
        self.assertEqual(
            leaf_node.props,
            None
        )

    def test_textnode_code_text(self):
        node = TextNode("Code Text", TextType.CODE, None) 
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(
            leaf_node.tag,
            "code"
        )
        self.assertEqual(
            leaf_node.value,
            "Code Text"
        )
        self.assertEqual(
            leaf_node.props,
            None
        )
    
    def test_textnode_link_text(self):
        node = TextNode("Link Text", TextType.LINK, "https://google.com") 
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(
            leaf_node.tag,
            "a"
        )
        self.assertEqual(
            leaf_node.value,
            "Link Text"
        )
        self.assertEqual(
            leaf_node.props["href"],
            "https://google.com"
        )
    
    def test_textnode_image_text(self):
        node = TextNode("Img Alt Text", TextType.IMAGE, "./media/rando.png") 
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(
            leaf_node.tag,
            "img"
        )
        self.assertEqual(
            leaf_node.value,
            ""
        )
        self.assertEqual(
            leaf_node.props["src"],
            "./media/rando.png"
        )
        self.assertEqual(
            leaf_node.props["alt"],
            "Img Alt Text"
        )


if __name__ == "__main__":
    unittest.main()