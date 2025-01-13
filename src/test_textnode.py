import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()