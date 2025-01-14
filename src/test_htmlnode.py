import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_create_empty(self):
        html_node = HTMLNode()
        self.assertIsNone(html_node.tag)
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.children)
        self.assertIsNone(html_node.props)

    def test_htmlnode_properties(self):
        props_dict = {"href":"https://www.google.com", "target":"_blank"}
        html_node = HTMLNode("<p>", "this is a paragraph", None, props_dict)
        self.assertEqual(html_node.tag, "<p>")
        self.assertEqual(html_node.value, "this is a paragraph")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, props_dict)

    def test_repr(self):
        props_dict = {"href":"https://www.google.com", "target":"_blank"}
        html_node = HTMLNode("<p>", "this is a paragraph", None, props_dict)
        self.assertEqual(
            f"HTMLNode(<p>, this is a paragraph, None, {props_dict})", repr(html_node)
        )

    def test_to_html(self):
        props_dict = {"href":"https://www.google.com", "target":"_blank"}
        html_node = HTMLNode("<a>", "Anchor", None, props_dict) 
        with self.assertRaises(NotImplementedError):
            html_node.to_html()
    
    def test_props_to_html_empty(self):
        html_node = HTMLNode("<a>", "Anchor", None, None)
        self.assertEqual(
            "", html_node.props_to_html()
        )

    def test_props_to_html_typeerror(self):
        html_node = HTMLNode("<a>", "Anchor", None, "wrong prop type")
        with self.assertRaises(TypeError):
           html_node.props_to_html() 

    def test_props_to_html(self):
        props_dict = {"href":"https://www.google.com", "target":"_blank"}
        html_node = HTMLNode("<a>", "Anchor", None, props_dict)
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', html_node.props_to_html()
        )

    
if __name__ == "__main__":
    unittest.main()