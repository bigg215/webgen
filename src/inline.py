from textnode import (TextNode,
					  text_type_text,
					  text_type_bold,
					  text_type_italic,
					  text_type_code,
					  text_type_link,
					  text_type_image,)
from parentnode import ParentNode
from textnode import TextNode, text_node_to_html
import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered = "unordered_list"
block_type_ordered = "ordered_list"


def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	children = []
	for block in blocks:
		html_node = block_to_html_node(block)
		children.append(html_node)
	return ParentNode("div", children, None)

def block_to_html_node(block):
	block_type = block_to_block_type(block)
	return func_to_html[block_type](block)

def text_to_children(text):
	text_nodes = text_to_textnodes(text)
	children = []
	for text_node in text_nodes:
		html_node = text_node_to_html(text_node)
		children.append(html_node)
	return children

def paragraph_to_html_node(block):
	text = " ".join(block.split("\n"))
	children = text_to_children(text)
	return ParentNode("p", children)

def heading_to_html_node(block):
	level = 0
	for char in block:
		if char == "#":
			level += 1
		else:
			break
	if level + 1 >= len(block):
		raise ValueError(f"invalid heading level: {level}")
	text = block[level+1:]
	children = text_to_children(text)
	return ParentNode(f"h{level}", children)

def code_to_html_node(block):
	text = block[3:-3]
	children = text_to_children(text)
	code = ParentNode("code", children)
	return ParentNode("pre", [code])

def olist_to_html_node(block):
	items = block.split("\n")
	html_items = []
	for item in items:
		text = item[3:]
		children = text_to_children(text)
		html_items.append(ParentNode("li", children))
	return ParentNode("ol", html_items)

def ulist_to_html_node(block):
	items = block.split("\n")
	html_items = []
	for item in items:
		text = item[2:]
		children = text_to_children(text)
		html_items.append(ParentNode("li", children))
	return ParentNode("ul", html_items)

def quote_to_html_node(block):
	lines = block.split("\n")
	new_lines = []
	for line in lines:
		if line[0] not in ">":
			raise ValueError("invalid quote block")
		new_lines.append(line.lstrip(">").strip())
	content = " ".join(new_lines)
	children = text_to_children(content)
	return ParentNode("blockquote", children)

func_to_html = {
	block_type_paragraph: paragraph_to_html_node,
	block_type_heading: heading_to_html_node,
	block_type_code: code_to_html_node,
	block_type_quote: quote_to_html_node,
	block_type_unordered: ulist_to_html_node,
	block_type_ordered: olist_to_html_node
}

def text_to_textnodes(text):
	nodes = [TextNode(text, text_type_text)]
	nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
	nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
	nodes = split_nodes_delimiter(nodes, "`", text_type_code)
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != text_type_text:
			new_nodes.append(old_node)
			continue
		split_nodes = []
		sections = old_node.text.split(delimiter)
		if len(sections) %2 == 0:
			raise ValueError("invalid md: missing closing tag")
		for i in range(len(sections)):
			if sections[i] == "":
				continue
			if i % 2 == 0:
				split_nodes.append(TextNode(sections[i], text_type_text))
			else:
				split_nodes.append(TextNode(sections[i], text_type))
		new_nodes.extend(split_nodes)
	return new_nodes

def split_nodes_image(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != text_type_text:
			new_nodes.append(old_node)
			continue
		original_text = old_node.text
		images = extract_markdown_images(original_text)
		if len(images) == 0:
			new_nodes.append(old_node)
			continue
		for image in images:
			sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
			if len(sections) != 2:
				raise ValueError("invalid markdown: missing closure")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], text_type_text))
			new_nodes.append(TextNode(image[0], text_type_image, image[1]))
			original_text = sections[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, text_type_text))
	return new_nodes


def split_nodes_link(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != text_type_text:
			new_nodes.append(old_node)
			continue
		original_text = old_node.text
		links = extract_markdown_links(original_text)
		if len(links) == 0:
			new_nodes.append(old_node)
			continue
		for link in links:
			sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
			if len(sections) != 2:
				raise ValueError("invalid markdown: missing closure")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], text_type_text))
			new_nodes.append(TextNode(link[0], text_type_link, link[1]))
			original_text = sections[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, text_type_text))
	return new_nodes


def extract_markdown_images(text):
	pattern = "!\[(.*?)\]\((.*?)\)"
	result = re.findall(pattern, text)
	return result

def extract_markdown_links(text):
	pattern = "(?<!!)\[(.*?)\]\((.*?)\)"
	result = re.findall(pattern, text)
	return result

def markdown_to_blocks(markdown):
	blocks = list(filter(len, markdown.split("\n\n")))
	blocks = list(map(str.strip, blocks))
	return blocks

def block_to_block_type(block):
	
	if block[0] == "#":
		sections = block.split()
		if sections[0] == len(sections[0]) * "#" and len(sections[0]) <= 6:
			return block_type_heading
		else:
			raise ValueError(f"invalid heading level: {len(sections[0])}")
		
	if block[:3] == "```" and block[-3:] == "```":
		return block_type_code
	
	if block[:2] == "* " or block[:2] == "- ":
		sections = block.split("\n")
		if all(list(map(lambda x: "* " in x[:2] or "- " in x[:2], sections))):
			return block_type_unordered
	
	if block[0] == ">":
		sections = block.split("\n")
		if all(list(map(lambda x: ">" in x[0], sections))):
			return block_type_quote
	
	if block[:3] == "1. ":
		sections = block.split("\n")
		count = 1
		for section in sections:
			if section[:3] == f"{count}. ":
				count += 1
			else:
				raise ValueError(f"invalid ordered list count: {count}")
		return block_type_ordered
	return block_type_paragraph