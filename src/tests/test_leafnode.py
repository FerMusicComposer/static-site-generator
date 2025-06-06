import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello, world")
        self.assertEqual(node.to_html(), "<p>Hello, world</p>")

    def test_to_html_with_props(self):
        node = LeafNode("p", "Hello, world", {"class": "container"})
        self.assertEqual(node.to_html(), "<p class=\"container\">Hello, world</p>")

    def test_no_tag_returns_raw_value(self):
        node = LeafNode(value="Hello, world")
        self.assertEqual(node.to_html(), "Hello, world")    

if __name__ == "__main__":
    unittest.main()