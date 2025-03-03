from leafnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

def text_node_to_html(text_node):
	types = [ 
		"text",
		"bold",
		"italic",
		"code",
		"link",
		"image",
	]
	if text_node.text_type not in types:
		raise Exception("invalid text node type")
	if text_node.text_type == "text":
		return LeafNode(None, text_node.text)
	if text_node.text_type == "bold":
		return LeafNode("b", text_node.text)
	if text_node.text_type == "italic":
		return LeafNode("i", text_node.text)
	if text_node.text_type == "code":
		return LeafNode("code", text_node.text)
	if  text_node.text_type == "link":
		return LeafNode("a", text_node.text, {"href":text_node.url})
	if text_node.text_type == "image":
		return LeafNode("img", "", {"src":text_node.text, "alt":text_node.url})

class TextNode():

	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url
	
	def __eq__(self, other):
		return (
			self.text == other.text
			and self.text_type == other.text_type
			and self.url == other.url
		)
	
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"
