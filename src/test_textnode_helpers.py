import unittest

from textnode_helpers import split_nodes_delimiter, is_textnode, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type
from textnode_helpers import BlockType
from textnode_helpers import markdown_to_html_node
from textnode_helpers import extract_title
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
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_splitnodes_code_block_at_start(self):
        node = TextNode("`A code block` starts this text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertListEqual(
            [
                TextNode("A code block", TextType.CODE),
                TextNode(" starts this text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_splitnodes_multi_node_list(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This sentence includes **bolded** text and a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This sentence includes **bolded** text and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE)
            ],
            new_nodes,
        )

    def test_splitnodes_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_splitnodes_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_empty_text_string(self):
        input_txt = ""
        with self.assertRaises(Exception) as cm:
            extract_markdown_images(input_txt)
        raised_exception = cm.exception
        self.assertEqual(
            raised_exception.args[0],
            "Input text string cannot be null or emtpy"
        )
    
    def test_single_image_return_list_tuples(self):
        input_txt = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = extract_markdown_images(input_txt)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertListEqual(
            [
                ("rick roll","https://i.imgur.com/aKaOqIh.gif")
            ],
            result,
        )
    
    def test_multi_image_return_list_tuples(self):
        input_txt = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(input_txt)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[1], tuple)
        self.assertListEqual(
            [
                ("rick roll","https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            result,
        )

    def test_empty_alt_text(self):
        input_txt = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif)"
        result = extract_markdown_images(input_txt)
        self.assertIsInstance(result, list)
        self.assertListEqual(
            [
                ("","https://i.imgur.com/aKaOqIh.gif")
            ],
            result,
        )

    def test_no_images(self):
        input_txt = "This is text with no images"
        result = extract_markdown_images(input_txt)
        self.assertIsInstance(result, list)
        self.assertListEqual(result, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_empty_text_string(self):
        input_txt = ""
        with self.assertRaises(Exception) as cm:
            extract_markdown_links(input_txt)
        raised_exception = cm.exception
        self.assertEqual(
            raised_exception.args[0],
            "Input text string cannot be null or emtpy"
        )
    
    def test_single_link_return_list_tuples(self):
        input_txt = "This is text with a link [to boot dev](https://www.boot.dev)"
        result = extract_markdown_links(input_txt)
        self.assertIsInstance(result, list)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev")

            ],
            result,
        )
    
    def test_multi_link_return_list_tuples(self):
        input_txt = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(input_txt)
        self.assertIsInstance(result, list)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            result,
        )

    def test_empty_anchor_text(self):
        input_txt = "This is text with an empty anchor that points to [](https://www.google.com)"
        result = extract_markdown_links(input_txt)
        self.assertIsInstance(result, list)
        self.assertListEqual(
            [
                ("","https://www.google.com")
            ],
            result,
        )

class TestSplitImages(unittest.TestCase):

    def test_split_images_no_image(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_image_at_beginning(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_three_images(self):
        node = TextNode(
            "This text has 3 images - ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), and ![one more](https://i.imgur.com/monkey.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text has 3 images - ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(", and ", TextType.TEXT),
                TextNode("one more", TextType.IMAGE, "https://i.imgur.com/monkey.png"),
            ],
            new_nodes,
        )

    def test_split_images_side_by_side(self):
        node = TextNode(
            "This is text with images ![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png) side by side",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with images ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" side by side", TextType.TEXT),
            ],
            new_nodes,
        )
class TestSplitLinks(unittest.TestCase):

    def test_split_link_no_link(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link to google](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    # test with link at the beginning
    def test_split_links_link_at_beginning(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [link to google](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    # test links side by side in the middle
    def test_split_links_side_by_side(self):
        node = TextNode(
            "This is text with links [link](https://i.imgur.com/zjjcJKZ.png) [link to google](https://google.com) side by side",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with links ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("link to google", TextType.LINK, "https://google.com"),
                TextNode(" side by side", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):

    def test_texttotextnodes_standard(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_texttotextnodes_no_bold(self):
        text = "This is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def text_texttotextnodes_multiple_images(self):
        text = "This is text with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and another ![yoda image](https://i.imgur.com/xyz123.jpeg)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("yoda image", TextType.IMAGE, "https://i.imgur.com/xyz123.jpeg"),
            ],
            new_nodes,
        )

    # test multiple links
    def text_texttotextnodes_multiple_links(self):
        text = "This is text with a [link to boot.dev](https://boot.dev) and another [link to google](https://google.com)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link to google", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_whitespace(self):
        md = """
This is **bolded** paragraph

 This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

 - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_double_newlines(self):
        md = """
This is **bolded** paragraph with a blank whitespace below:

 

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

 - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph with a blank whitespace below:",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
class TestBlockToBlockType(unittest.TestCase):

    def test_heading_one(self):
        md_block = "# This is a heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_heading_two(self):
        md_block = "## This is a heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_heading_three(self):
        md_block = "### This is a heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_heading_four(self):
        md_block = "#### This is a heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_heading_five(self):
        md_block = "##### This is a heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_heading_six(self):
        md_block = "###### This is a heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_code_block(self):
        md_block = "```python\nprint('Hello World')\n```"
        block_type = block_to_block_type(md_block)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )

    def test_quote_block(self):
        md_block = "> This is a quote"
        block_type = block_to_block_type(md_block)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )

    def test_multi_quote_block(self):
        md_block = "> This is a quote\n> with multiple lines"
        block_type = block_to_block_type(md_block)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        md_block = """
- This is the first item in the list
- This is the second item in the list
- This is the third item in the list
"""
        block_type = block_to_block_type(md_block)

        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )

    def test_unordered_list_malformed(self):
        md_block = """
- This is the first item in the list
This is the second item in the list
- This is the third item in the list
"""
        block_type = block_to_block_type(md_block)

        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_ordered_list_well_formed(self):
        # Every line in an ordered list block must start with a number followed by a . character and a space. 
        # The number must start at 1 and increment by 1 for each line.
        md_block = """
1. This is the first item in the list
2. This is the second item in the list
3. This is the third item in the list
"""
        block_type = block_to_block_type(md_block)

        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )

    def test_ordered_list_malformed(self):
        md_block = """
1. This is the first line
3. This is the second line
2. This is the third line
"""

        block_type = block_to_block_type(md_block)

        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_paragraph(self):
        md_block = """
This is a paragraph with multiple lines.
It should be recognized as a paragraph block.
"""
        block_type = block_to_block_type(md_block)

        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_list_items(self):
        md = """
- Item 1
- Item 2
- Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list_items(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )

    def test_ordered_list_items_inline_elements(self):
        md = """
1. Item with some _italic_ text
2. Item with some **bold** text
3. Item with some `code` text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item with some <i>italic</i> text</li><li>Item with some <b>bold</b> text</li><li>Item with some <code>code</code> text</li></ol></div>",
        )

    def test_unordered_list_items_inline_elements(self):
        md = """
- Item with some _italic_ text
- Item with some **bold** text
- Item with some `code` text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item with some <i>italic</i> text</li><li>Item with some <b>bold</b> text</li><li>Item with some <code>code</code> text</li></ul></div>",
        )

class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
     
"""
        title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")

    def test_extract_title_no_h1(self):
        md = "This is not a title"
        with self.assertRaises(ValueError) as cm:
            extract_title(md)
        raised_exception = cm.exception
        self.assertEqual(
            raised_exception.args[0],
            "No H1 header [#] found in provided markdown"
        )

if __name__ == "__main__":
    unittest.main()