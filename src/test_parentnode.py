import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
	
	def test_eq(self):
		node = ParentNode(
		"p",
		[
			LeafNode("b", "Bold text")
		],
		)
		node2 = ParentNode(
		"p",
		[
			LeafNode("b", "Bold text")
		],
		)
		self.assertEqual(node, node2)
	def test_not_eq(self):
		node = ParentNode(
		"p",
		[
			LeafNode("b", "Bold text"),
			LeafNode("b", "Bold text")
		],
		)
		node2 = ParentNode(
		"p",
		[
			LeafNode("b", "Bold text")
		],
		)
		self.assertNotEqual(node, node2)
	def test_no_tag(self):
		node = ParentNode(
		None,
		[
			LeafNode("b", "Bold text")
		],
		)
		self.assertRaises(ValueError)
	def test_no_children(self):
		node = ParentNode("p", None)
		self.assertRaises(ValueError)
	def test_to_html(self):
		node = ParentNode(
		"p",
		[
			LeafNode("b", "Bold text"),
			LeafNode(None, "Normal text"),
			LeafNode("i", "italic text"),
			LeafNode(None, "Normal text"),
		],
		)
		expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
		self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()