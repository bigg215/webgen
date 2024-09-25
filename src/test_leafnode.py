import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
	def test_eq(self):
		node = LeafNode("a", "text", {"href": "https://www.google.com"})
		node2 = LeafNode("a", "text", {"href": "https://www.google.com"})
		self.assertEqual(node, node2)
	def test_not_eq(self):
		node = LeafNode("a", "text",)
		node2 = LeafNode("a", "text", {"href": "https://www.google.com"})
		self.assertNotEqual(node, node2)
	def test_no_value(self):
		node = LeafNode('a', None, {"href": "https://www.google.com"})
		self.assertRaises(ValueError)
	def test_no_tag(self):
		plain_text = "plain text"
		node = LeafNode(None, plain_text, {"href": "https://www.google.com"} )
		self.assertEqual(node.to_html(), plain_text)
	def test_to_html(self):
		compare = '<a href="https://www.google.com">link</a>'
		node = LeafNode("a", "link", {"href": "https://www.google.com"})
		self.assertEqual(node.to_html(), compare)

if __name__ == "__main__":
    unittest.main()