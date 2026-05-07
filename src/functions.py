import re

from textnode import TextType, TextNode

def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # This function only process TEXT nodes. If other type, means it has already been processed and converted to the appropriate type
        if node.text_type == TextType.TEXT:
            # Applying delimiter
            strings = node.text.split(delimiter)
            # If the result after .split() is even, it means the delimiters are unmatched
            if len(strings) % 2 == 0:
                raise Exception("incorrect Markdown format, unmatched delimiters")
            # If the result is 1, it means there are no delimiters so it has to be passed as TEXT
            if len(strings) == 1:
                new_nodes.append(TextNode(strings[0], TextType.TEXT))
            else:
                for i in range(len(strings)):
                    # Even strings are the ones outside delimiters
                    if i % 2 == 0:
                        if strings[i] != "":
                            new_nodes.append(TextNode(strings[i], TextType.TEXT))
                    # Odd strings are the ones delimited
                    else:
                        new_nodes.append(TextNode(strings[i], text_type))            
        else:
            # Node is not TEXT
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    data = []
    # Regex pattern to find image links ![alt_text](url)
    matches = re.findall(r"!\[[^\]]+\]\([\w.:/]+\)", text)
    for match in matches:
        # For each match, separate the alt_text and the url parts. Strip the leading and trailing [] and ()
        alt = re.search(r"\[.*\]", match).group().lstrip("[").rstrip("]")
        url = re.search(r"\(.*\)", match).group().lstrip("(").rstrip(")")
        # Append to the list as a tuple
        data.append((alt, url))
    return data
    

def extract_markdown_links(text):
    data = []
    # Regex pattern to find image links [anchor_text](url)
    matches = re.findall(r"(?<!\!)\[[^\]]+\]\([\w.:/]+\)", text)
    for match in matches:
        # For each match, separate the anchor_text and the url parts. Strip the leading and trailing [] and ()
        anchor_text = re.search(r"\[.*\]", match).group().lstrip("[").rstrip("]")
        url = re.search(r"\(.*\)", match).group().lstrip("(").rstrip(")")
        # Append to the list as a tuple
        data.append((anchor_text, url))
    return data


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Id node is not TEXT, it means it has already been handled
        if node.text_type == TextType.TEXT:
            # Getting image data tuples from Markdown matches
            image_tuples = extract_markdown_images(node.text)
            # remaining_text starts being the whole text of the current node.
            # For each image tuple iteration, the text is split using the strings from tuple. 
            # From the .split() result, the first string is the next TEXT node. The second is the IMAGE node
            # The remaining text gets stored for the next tuple iteration.
            remaining_text = node.text
            for alt, url in image_tuples:
                delimiter = f"![{alt}]({url})"
                strings = remaining_text.split(delimiter, 1)
                if strings[0] != "":
                    new_nodes.append(TextNode(strings[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                remaining_text = strings[1]
            # When there're no more tuples, the remaining text is the trailing characters after the last image node
            # It's appended as TEXT node if it's not empty
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))    
        else:
            # If node is not TEXT
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            link_tuples = extract_markdown_links(node.text)
            # See split_nodes_image() for info
            remaining_text = node.text
            for anchor, url in link_tuples:
                delimiter = f"[{anchor}]({url})"
                strings = remaining_text.split(delimiter, 1)
                if strings[0] != "":
                    new_nodes.append(TextNode(strings[0], TextType.TEXT))
                new_nodes.append(TextNode(anchor, TextType.LINK, url))
                remaining_text = strings[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))    
        else:
            # Node is not TEXT
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_node_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_node_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_node_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    