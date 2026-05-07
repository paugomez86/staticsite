import unittest

from textnode import TextNode, TextType
from functions import split_node_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes 

class TestFunctions(unittest.TestCase):
    def test_delimiter(self):
        nodes = [TextNode("`code` with plain text and **bold**", TextType.TEXT), TextNode("plain text with _italic text_", TextType.TEXT)]
        nodes = split_node_delimiter(nodes, "`", TextType.CODE)
        nodes = split_node_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_node_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 5)
    
    def test_no_delimiter(self):
        node = [TextNode("text without delimiters", TextType.TEXT)]
        new_node = split_node_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(new_node, node)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)\n" + 
            "This is text with ![another image](https://i.imgur.com/zjjcJKZ.png)\n" +
            "This is text with ![random characters...---](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("another image", "https://i.imgur.com/zjjcJKZ.png"),
            ("random characters...---", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an anchor: [Download here](https://i.imgur.com/zjjcJKZ.png)\n" +
            "Another anchor: [Download here](https://i.imgur.com/zjjcJKZ.png)\n" +
            "[Download here](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("Download here", "https://i.imgur.com/zjjcJKZ.png"),
            ("Download here", "https://i.imgur.com/zjjcJKZ.png"),
            ("Download here", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)


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
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link!!](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link!!", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes(self):
        text = ("Long text with all kinds of characters!! Does it work? It has **bold** and _italic_. " +
        "There is some `code blocks here` and `there`. More **bold text**, a [link](boot.dev) and an ![image](/images/image.png)" +
        "![Another image alt text](/images/image.png) with more _italic text_. And some `extra code`")
        
        nodes = text_to_textnodes(text)
        
        self.assertListEqual(
            [
                TextNode("Long text with all kinds of characters!! Does it work? It has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(". There is some ", TextType.TEXT),
                TextNode("code blocks here", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("there", TextType.CODE),
                TextNode(". More ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(", a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode(" and an ", TextType.TEXT) ,
                TextNode("image", TextType.IMAGE, "/images/image.png"),
                TextNode("Another image alt text", TextType.IMAGE, "/images/image.png"),
                TextNode(" with more ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(". And some ", TextType.TEXT),
                TextNode("extra code", TextType.CODE),
            ],
            nodes
        )
        
if __name__ == "__main__":
    unittest.main()