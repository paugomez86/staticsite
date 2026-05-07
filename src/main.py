from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import split_node_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, text_to_textnodes

text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"


nodes = text_to_textnodes(text)
for item in nodes:
    print(item)

