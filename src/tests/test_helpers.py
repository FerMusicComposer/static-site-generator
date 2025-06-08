import unittest
from texnode import TextNode, TextType
from helpers import *

class TestHelpers(unittest.TestCase):
    def test_split_single_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_multiple_code_blocks(self):
        node = TextNode("Some `code1` and also `code2` here.", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("Some ", TextType.NORMAL),
            TextNode("code1", TextType.CODE),
            TextNode(" and also ", TextType.NORMAL),
            TextNode("code2", TextType.CODE),
            TextNode(" here.", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_delimiter_found(self):
        node = TextNode("This is plain text.", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`start code` middle text `end code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("start code", TextType.CODE),
            TextNode(" middle text ", TextType.NORMAL),
            TextNode("end code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_missing_closing_delimiter(self):
        node = TextNode("This is text with a `code block missing end", TextType.NORMAL)
        with self.assertRaisesRegex(ValueError, "Invalid Markdown syntax: closing delimiter '`' not found in 'This is text with a `code block missing end'"):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_different_delimiter_bold(self):
        node = TextNode("This is **bold text** in a sentence.", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in a sentence.", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_different_delimiter_italic(self):
        node = TextNode("Here's _some italic_ words.", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("Here's ", TextType.NORMAL),
            TextNode("some italic", TextType.ITALIC),
            TextNode(" words.", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_mixed_nodes_input(self):
        node1 = TextNode("Normal text", TextType.NORMAL)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("Text with `code` block", TextType.NORMAL)
        node4 = TextNode("Already italic", TextType.ITALIC)

        old_nodes = [node1, node2, node3, node4]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)

        expected_nodes = [
            TextNode("Normal text", TextType.NORMAL),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Text with ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.NORMAL),
            TextNode("Already italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_empty_string_between_delimiters(self):
        node = TextNode("Prefix**bold**Suffix", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Prefix", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode("Suffix", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
        node_no_prefix = TextNode("**bold**Suffix", TextType.NORMAL)
        new_nodes_no_prefix = split_nodes_delimiter([node_no_prefix], "**", TextType.BOLD)
        expected_nodes_no_prefix = [
            TextNode("bold", TextType.BOLD),
            TextNode("Suffix", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes_no_prefix, expected_nodes_no_prefix)

        node_no_suffix = TextNode("Prefix**bold**", TextType.NORMAL)
        new_nodes_no_suffix = split_nodes_delimiter([node_no_suffix], "**", TextType.BOLD)
        expected_nodes_no_suffix = [
            TextNode("Prefix", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes_no_suffix, expected_nodes_no_suffix)

    def test_delimiter_in_middle_of_word(self):
        node = TextNode("hello`world`goodbye", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("hello", TextType.NORMAL),
            TextNode("world", TextType.CODE),
            TextNode("goodbye", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_extract_markdown_images_single(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_extract_markdown_images_multiple(self):
        text = "This is text with ![image1](url1.jpg) and also ![image2](url2.png)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("image1", "url1.jpg"), ("image2", "url2.png")])

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images or links."
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

    def test_extract_markdown_images_mixed_content(self):
        text = "Here's an image ![alt](img.jpeg) and a link [link](url.com)."
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt", "img.jpeg")])

    def test_extract_markdown_images_empty_alt_text_url(self):
        text = "Image with empty alt text: ![](/path/to/image.png) and empty URL: ![empty]()."
        images = extract_markdown_images(text)
        self.assertEqual(images, [("", "/path/to/image.png"), ("empty", "")])

    def test_extract_markdown_images_special_chars(self):
        text = "![Alt text with spaces and-hyphens](https://example.com/image_with_underscores.gif?param=value)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("Alt text with spaces and-hyphens", "https://example.com/image_with_underscores.gif?param=value")])

    def test_extract_markdown_links_single(self):
        text = "Visit [Google](https://www.google.com) for search."
        links = extract_markdown_links(text)
        self.assertEqual(links, [("Google", "https://www.google.com")])

    def test_extract_markdown_links_multiple(self):
        text = "My favorite sites are [GitHub](https://github.com) and [Stack Overflow](https://stackoverflow.com)."
        links = extract_markdown_links(text)
        self.assertEqual(links, [("GitHub", "https://github.com"), ("Stack Overflow", "https://stackoverflow.com")])

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links at all."
        links = extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_extract_markdown_links_mixed_content_with_images(self):
        text = "An image ![alt](img.jpg) and a link [blog](https://blog.example.com)."
        links = extract_markdown_links(text)
        self.assertEqual(links, [("blog", "https://blog.example.com")])

    def test_extract_markdown_links_special_chars(self):
        text = "[Link with spaces & hyphens](https://example.org/path/to/page?query=test&param=value)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("Link with spaces & hyphens", "https://example.org/path/to/page?query=test&param=value")])

    def test_extract_markdown_links_image_like_but_not_image(self):
        text = "This is not an image but a link: [!important link](http://example.com/not-an-image)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("!important link", "http://example.com/not-an-image")])

if __name__ == "__main__":
    unittest.main()
