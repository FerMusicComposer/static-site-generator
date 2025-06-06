import unittest
from htmlnode import HtmlNode
from leafnode import LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode("div", "Hello", [], {"class": "container"})
        self.assertEqual(node.props_to_html(), 'class="container"')

    def test_self_repr(self):
        node = HtmlNode("div", "Hello", [], {"class": "container"})
        self.assertEqual(repr(node), "HtmlNode(div, Hello, [], {'class': 'container'})")
 
    def test_children_is_valid_htmlnode(self):
        node = HtmlNode("div", "Hello", [
            HtmlNode("p", "This is a test")
        ], {"class": "container"})
        self.assertIsInstance(node.children[0], HtmlNode)
