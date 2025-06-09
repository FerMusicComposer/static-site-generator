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

    def test_split_nodes_image_single(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png).", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is plain text with no images.", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_nodes_image_image_at_start(self):
        node = TextNode("![start image](url.png) This text follows.", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("start image", TextType.IMAGE, "url.png"),
            TextNode(" This text follows.", TextType.NORMAL),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_image_at_end(self):
        node = TextNode("This text ends with an ![end image](url.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This text ends with an ", TextType.NORMAL),
            TextNode("end image", TextType.IMAGE, "url.jpg"),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_only_image(self):
        node = TextNode("![full image](full.gif)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("full image", TextType.IMAGE, "full.gif"),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_mixed_input_nodes(self):
        node1 = TextNode("Text with ![img1](u1.png)", TextType.NORMAL)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("Another ![img2](u2.jpg) here", TextType.NORMAL)
        node4 = TextNode("Already link", TextType.LINK, "http://example.com")

        old_nodes = [node1, node2, node3, node4]
        new_nodes = split_nodes_image(old_nodes)

        expected_nodes = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("img1", TextType.IMAGE, "u1.png"),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Another ", TextType.NORMAL),
            TextNode("img2", TextType.IMAGE, "u2.jpg"),
            TextNode(" here", TextType.NORMAL),
            TextNode("Already link", TextType.LINK, "http://example.com"),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_with_empty_alt_text_url(self):
        node = TextNode("Empty alt: ![](/path/to/img.png) Empty URL: ![no-url]()", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("Empty alt: ", TextType.NORMAL),
            TextNode("", TextType.IMAGE, "/path/to/img.png"),
            TextNode(" Empty URL: ", TextType.NORMAL),
            TextNode("no-url", TextType.IMAGE, ""),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_single(self):
        node = TextNode("This is text with a [Google](https://www.google.com).", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is plain text with no links.", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_nodes_link_link_at_start(self):
        node = TextNode("[start link](url.com) This text follows.", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("start link", TextType.LINK, "url.com"),
            TextNode(" This text follows.", TextType.NORMAL),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_link_at_end(self):
        node = TextNode("This text ends with a [end link](url.org)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This text ends with a ", TextType.NORMAL),
            TextNode("end link", TextType.LINK, "url.org"),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_only_link(self):
        node = TextNode("[full link](full.net)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("full link", TextType.LINK, "full.net"),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_mixed_input_nodes(self):
        node1 = TextNode("Text with [link1](l1.com)", TextType.NORMAL)
        node2 = TextNode("Already image", TextType.IMAGE, "http://image.com/img.png")
        node3 = TextNode("Another [link2](l2.org) here", TextType.NORMAL)
        node4 = TextNode("Already bold", TextType.BOLD)

        old_nodes = [node1, node2, node3, node4]
        new_nodes = split_nodes_link(old_nodes)

        expected_nodes = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("link1", TextType.LINK, "l1.com"),
            TextNode("Already image", TextType.IMAGE, "http://image.com/img.png"),
            TextNode("Another ", TextType.NORMAL),
            TextNode("link2", TextType.LINK, "l2.org"),
            TextNode(" here", TextType.NORMAL),
            TextNode("Already bold", TextType.BOLD),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_with_empty_link_text_url(self):
        node = TextNode("Empty text: [][http://empty.com] Empty URL: [no-url]()", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Empty text: [][http://empty.com] Empty URL: ", TextType.NORMAL),
            TextNode("no-url", TextType.LINK, ""),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_image_in_text_not_split(self):
        node = TextNode("This text has an ![image](url.png) but should only split [links](link.com).", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This text has an ![image](url.png) but should only split ", TextType.NORMAL),
            TextNode("links", TextType.LINK, "link.com"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_text_to_textnodes_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_textnodes_only_normal_text(self):
        text = "This is a plain sentence with no formatting."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is a plain sentence with no formatting.", TextType.NORMAL)
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_textnodes_single_type(self):
        text_bold = "Only **bold** here."
        nodes_bold = text_to_textnodes(text_bold)
        expected_nodes_bold = [
            TextNode("Only ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" here.", TextType.NORMAL),
        ]
        self.assertListEqual(nodes_bold, expected_nodes_bold)

        text_image = "Just an ![image](image.png)."
        nodes_image = text_to_textnodes(text_image)
        expected_nodes_image = [
            TextNode("Just an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "image.png"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(nodes_image, expected_nodes_image)

    def test_text_to_textnodes_complex_mix(self):
        text = "**Bold start** _italic_ middle `code` end. Also an ![img](u.jpg) and a [link](l.com)."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Bold start", TextType.BOLD),
            TextNode(" _italic_ middle `code` end. Also an ", TextType.NORMAL), # Intermediate string after bold split
            TextNode("img", TextType.IMAGE, "u.jpg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "l.com"),
            TextNode(".", TextType.NORMAL)
        ]
        # Re-evaluating the expected nodes after chained splits
        # The splitting order is important: images -> links -> code -> bold -> italic
        text = "**Bold start** _italic_ middle `code` end. Also an ![img](u.jpg) and a [link](l.com)."
        
        # After images:
        # ['**Bold start** _italic_ middle `code` end. Also an ', TextNode(img, IMAGE, u.jpg), ' and a [link](l.com).']
        nodes = text_to_textnodes(text)
        # After links: (from the result of images)
        # TextNode("Bold start", BOLD) is still normal type before delimiter split
        # TextNode(" and a ", TextType.NORMAL) is also normal text
        # ...
        
        expected_nodes = [
            TextNode("Bold start", TextType.BOLD),
            TextNode(" ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" middle ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" end. Also an ", TextType.NORMAL),
            TextNode("img", TextType.IMAGE, "u.jpg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "l.com"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_textnodes_consecutive_markdown(self):
        text = "Hello `world`! **Important** _note_ this."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Hello ", TextType.NORMAL),
            TextNode("world", TextType.CODE),
            TextNode("! ", TextType.NORMAL),
            TextNode("Important", TextType.BOLD),
            TextNode(" ", TextType.NORMAL),
            TextNode("note", TextType.ITALIC),
            TextNode(" this.", TextType.NORMAL),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_textnodes_markdown_at_boundaries(self):
        text = "**Start** text [link](url.com) and `code` at _end_."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Start", TextType.BOLD),
            TextNode(" text ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" at ", TextType.NORMAL),
            TextNode("end", TextType.ITALIC),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
if __name__ == "__main__":
    unittest.main()
