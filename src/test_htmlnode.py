import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node = HTMLNode("a", "text", ['a'], {"href": "https://www.google.com"})
		node2 = HTMLNode("a", "text", ['a'], {"href": "https://www.google.com"})
		self.assertEqual(node, node2)
	def test_empty(self):
		node = HTMLNode()
		self.assertEqual(node.tag, None)
		self.assertEqual(node.value, None)
		self.assertEqual(node.children, None)
		self.assertEqual(node.props, None)
	def test_mismatch(self):
		node = HTMLNode()
		node2 = HTMLNode("a", "text", ['a'], {"href": "https://www.google.com"})
		self.assertNotEqual(node, node2)
if __name__ == "__main__":
    unittest.main()