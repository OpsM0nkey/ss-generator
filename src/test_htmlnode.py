import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_parentnode_create_empty_errors(self):
        with self.assertRaises(TypeError):
            parent_node = ParentNode()
    
    def test_parentnode_create_params(self):
        parent_node = ParentNode("p", LeafNode())
        self.assertEqual(parent_node.tag, "p")
        self.assertIsInstance(parent_node.children, LeafNode)
        self.assertIsNone(parent_node.props)

    def test_parentnode_valueerror_no_tag(self):
        parent_node = ParentNode(None, LeafNode())
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        raised_exception = cm.exception
        self.assertEqual(raised_exception.args[0], "Tag cannot be None or empty")

    def test_parentnode_valueerror_no_children(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        raised_exception = cm.exception
        self.assertEqual(raised_exception.args[0], "ParentNode must include a children property")

    def test_parentnode_recursion_tohtml(self):
        parent_node = ParentNode(
                        "p",
                        [
                            LeafNode("b", "Bold text"),
                            LeafNode(None, "Normal text"),
                            LeafNode("i", "italic text"),
                            LeafNode(None, "Normal text"),
                        ],)
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_recursion_includes_parents(self):
        parent_node = ParentNode(
                        "p",
                        [
                            LeafNode("b", "Bold text"),
                            LeafNode(None, "Normal text"),
                            LeafNode("i", "italic text"),
                            ParentNode("p", [
                                LeafNode(None, "Normal text")
                            ]),
                            LeafNode(None, "Normal text"),
                        ],)
        self.assertEqual(
            parent_node.to_html(), 
            "<p><b>Bold text</b>Normal text<i>italic text</i><p>Normal text</p>Normal text</p>"
        )
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    
if __name__ == "__main__":
    unittest.main()