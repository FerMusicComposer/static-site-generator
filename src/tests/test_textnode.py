import unittest
from texnode import TextType, TextNode
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_equal(self):
        node = TextNode("this is a bold text", TextType.BOLD)
        node2 = TextNode("this is a bold text", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("this is a bold text", TextType.BOLD)
        node2 = TextNode("this is a bold text", TextType.NORMAL)
        self.assertNotEqual(node, node2)
    
    def test_url_not_none_for_link(self):
        node = TextNode("this is a link", TextType.LINK, "https://google.com")
        self.assertIsNotNone(node.url)

    def test_url_not_none_for_image(self):
        node = TextNode("this is a bold text", TextType.IMAGE, "https://example.com/image.jpg")
        self.assertIsNotNone(node.url)

    def test_link_and_image_are_not_equal(self):
        node = TextNode("this is a link", TextType.LINK, "https://google.com")
        node2 = TextNode("this is a image", TextType.IMAGE, "https://example.com/image.jpg")
        self.assertNotEqual(node, node2)

    def test_text_node_to_leaf_node(self):
        node = TextNode("this is a bold text", TextType.BOLD)
        leaf_node = node.text_node_to_html_node()
        self.assertIsInstance(leaf_node, LeafNode)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "this is a bold text")

if __name__ == "__main__":
    unittest.main()