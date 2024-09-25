from htmlnode import HTMLNode

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)
	
	def to_html(self):
		if self.tag is None:
			raise ValueError("all parent nodes must have a tag")
		if self.children is None:
			raise ValueError("all parent nodes must have children")
		child_html = ""
		for child in self.children:
			child_html += child.to_html()
		return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'
	
	def __repr__(self):
		return f"ParentNode({self.tag}, {self.children}, {self.props})"