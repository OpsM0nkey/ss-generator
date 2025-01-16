import unittest

from htmlnode import HTMLNode, LeafNode

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

class TestLeafNode(unittest.TestCase):
    def test_leafnode_create_empty(self):
        leaf_node = LeafNode()
        self.assertIsNone(leaf_node.tag)
        self.assertEqual(leaf_node.value, "")
        self.assertIsNone(leaf_node.children)
        self.assertIsNone(leaf_node.props)

    def test_leafnode_no_children(self):
        props_dict = {"href":"https://www.google.com", "target":"_blank"}
        leaf_node = LeafNode(None,"basic paragraph", props_dict)
        self.assertIsNone(leaf_node.children)
        self.assertEqual(leaf_node.props, props_dict)

    def test_leafnode_value_none(self):
        leaf_node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()
    
    def test_leafnode_value_emptystring(self):
        leaf_node = LeafNode(None, "")
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_leafnode_tohtml_no_tag(self):
        leaf_node = LeafNode(None,"This is just raw text.", None)
        self.assertEqual(leaf_node.to_html(), "This is just raw text.")

    def test_leafnode_tag_noprops(self):
       leaf_node = LeafNode("p","This is a paragraph of text.", None)
       self.assertEqual(leaf_node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leafnode_tag_with_props(self):
       leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
       self.assertEqual(leaf_node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    
if __name__ == "__main__":
    unittest.main()