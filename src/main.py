from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        ParentNode("div", [
            LeafNode("h1", "title"),
            LeafNode("i", "italic text"),
        ], {"class": "container"}), 
        LeafNode(None, "Normal text"),
    ],
)

print(node.to_html())