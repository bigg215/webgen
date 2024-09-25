import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", "bold")
		node2 = TextNode("This is a text node", "bold")
		self.assertEqual(node, node2)
	def test_url_none(self):
		node = TextNode("xxx", "bold")
		self.assertEqual(node.url, None)
	def test_mismatch_type(self):
		node = TextNode("xxx", "bold")
		node2 = TextNode("xxx", "italics")
		self.assertNotEqual(node, node2)
	def test_mismatch_text(self):
		node = TextNode("123", "bold")
		node2 = TextNode("456", "bold")
		self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()