import unittest
import textwrap
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
    
    def test_markdown_to_blocks_start_end_no_extra_newlines(self):
        """
        Tests markdown_to_blocks with markdown that starts and ends precisely with blocks
        and has no excessive newlines.
        """
        md = """# Heading One
This is some text.

Another paragraph.
- List item 1
- List item 2
"""
        blocks = markdown_to_blocks(md)
        expected_blocks = [
            "# Heading One\nThis is some text.",
            "Another paragraph.\n- List item 1\n- List item 2",
        ]
        self.assertEqual(blocks, expected_blocks)

    def test_markdown_to_blocks_multiple_paragraphs_varying_newlines(self):
        """
        Tests markdown_to_blocks with multiple paragraphs and varying amounts of newlines
        between them to ensure correct trimming and block identification.
        """
        md = """First paragraph.

Second paragraph.


Third paragraph.


Fourth paragraph, no trailing newlines."""
        blocks = markdown_to_blocks(md)
        expected_blocks = [
            "First paragraph.",
            "Second paragraph.",
            "Third paragraph.",
            "Fourth paragraph, no trailing newlines."
        ]
        self.assertEqual(blocks, expected_blocks)

    def test_block_to_blocktype_paragraph(self):
        block = "This is a normal paragraph of text."
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)

    def test_block_to_blocktype_heading_h6(self):
        block = "###### This is a smaller heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)

    def test_block_to_blocktype_heading_invalid(self):
        self.assertEqual(block_to_blocktype("####### Not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("##No leading space"), BlockType.PARAGRAPH)


    def test_block_to_blocktype_code(self):
        block = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)
    
    def test_block_to_blocktype_code_single_line(self):
        block = "```console.log('hi')```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)

    def test_block_to_blocktype_code_missing_ticks(self):
        self.assertEqual(block_to_blocktype("```code without end"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("code without start```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("`single backtick`"), BlockType.PARAGRAPH) # Not a code block in this context

    def test_block_to_blocktype_quote(self):
        block = "> This is a quote\n> Another line of quote"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

    def test_block_to_blocktype_quote_single_line(self):
        block = "> Just one line."
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

    def test_block_to_blocktype_quote_invalid(self):
        block = "> Line 1\nLine 2 (not a quote)"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_unordered_list_hyphen(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_unordered_list_star(self):
        block = "* Item A\n* Item B"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH) 

    def test_block_to_blocktype_unordered_list_invalid(self):
        block = "- Item 1\nNot a list item"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
        block_no_space = "-Item No Space"
        self.assertEqual(block_to_blocktype(block_no_space), BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)

    def test_block_to_blocktype_ordered_list_invalid_number(self):
        block = "1. Item 1\n3. Item 2" # Skips 2
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list_invalid_format(self):
        self.assertEqual(block_to_blocktype("1.Item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("1- Item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype("0. Item"), BlockType.PARAGRAPH) # Should start at 1

    def test_block_to_blocktype_paragraph_with_hash_in_middle(self):
        block = "This is a paragraph with #hash in the middle."
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_paragraph_looks_like_list_item(self):
        block = "This is a sentence - that continues on."
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_complex_paragraph(self):
        block = "This is a paragraph.\nIt has multiple lines.\nAnd some content."
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_text_to_html_nodes_basic_conversion(self):
        text = "This is **bold** and _italic_ with `code`."
        nodes = text_to_html_nodes(text)
        expected_nodes = [
            LeafNode(None, "This is "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " with "),
            LeafNode("code", "code"),
            LeafNode(None, "."),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_text_to_html_nodes_with_images_links(self):
        text = "Check this ![image](img.jpg) and [this link](link.com)."
        nodes = text_to_html_nodes(text)
        expected_nodes = [
            LeafNode(None, "Check this "),
            LeafNode("img", "", {"src": "img.jpg", "alt": "image"}),
            LeafNode(None, " and "),
            LeafNode("a", "this link", {"href": "link.com"}),
            LeafNode(None, "."),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_text_to_html_nodes_only_normal_text(self):
        text = "Just plain text."
        nodes = text_to_html_nodes(text)
        expected_nodes = [
            LeafNode(None, "Just plain text."),
        ]
        self.assertEqual(nodes, expected_nodes)
    
    def test_text_to_html_nodes_empty_string(self):
        text = ""
        nodes = text_to_html_nodes(text)
        expected_nodes = []
        self.assertEqual(nodes, expected_nodes)

    def test_heading_block_to_html_node_h1(self):
        block = "# My Heading"
        node = heading_block_to_html_node(block)
        expected_node = ParentNode("h1", [LeafNode(None, "My Heading")])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_heading_block_to_html_node_h3_with_inline(self):
        block = "### Heading with **bold** and `code`"
        node = heading_block_to_html_node(block)
        expected_node = ParentNode("h3", [
            LeafNode(None, "Heading with "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("code", "code"),
        ])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_heading_block_to_html_node_invalid_level_too_high(self):
        block = "####### Too many hashes"
        with self.assertRaisesRegex(ValueError, r"Invalid heading level\. Must start with 1 to 6 hash characters: ####### Too many hashes"):
            heading_block_to_html_node(block)

    def test_code_block_to_html_node_multi_line(self):
        block = "```\nprint('Hello')\n```"
        node = code_block_to_html_node(block)
        expected_node = ParentNode("pre", [LeafNode("code", "print('Hello')")])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_code_block_to_html_node_single_line(self):
        block = "```console.log('test');```"
        node = code_block_to_html_node(block)
        expected_node = ParentNode("pre", [LeafNode("code", "console.log('test');")])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_code_block_to_html_node_invalid_no_closing(self):
        block = "```print('no close')"
        with self.assertRaisesRegex(ValueError, r"Invalid code block\. Must start with '```' and end with '```': ```print\('no close'\)"):
            code_block_to_html_node(block)

    def test_quote_block_to_html_node_multi_line(self):
        block = "> This is a quote.\n> Second line of quote."
        node = quote_block_to_html_node(block)
        expected_node = ParentNode("blockquote", [LeafNode(None, "This is a quote.\nSecond line of quote.")])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_quote_block_to_html_node_with_inline(self):
        block = "> This is _italic_ and **bold**."
        node = quote_block_to_html_node(block)
        expected_node = ParentNode("blockquote", [
            LeafNode(None, "This is "),
            LeafNode("i", "italic"),
            LeafNode(None, " and "),
            LeafNode("b", "bold"),
            LeafNode(None, "."),
        ])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_quote_block_to_html_node_invalid_line(self):
        block = "> Line 1\nLine 2 not quoted"
        with self.assertRaisesRegex(ValueError, "Invalid quote block. All lines must begin with a '>' character: Line 2 not quoted"):
            quote_block_to_html_node(block)

    def test_ul_block_to_html_node_basic(self):
        block = "- Item 1\n- Item 2"
        node = ul_block_to_html_node(block)
        expected_node = ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "Item 1")]),
            ParentNode("li", [LeafNode(None, "Item 2")]),
        ])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_ul_block_to_html_node_with_inline(self):
        block = "- Item **one**\n- Item _two_ with [link](url.com)"
        node = ul_block_to_html_node(block)
        expected_node = ParentNode("ul", [
            ParentNode("li", [
                LeafNode(None, "Item "),
                LeafNode("b", "one"),
            ]),
            ParentNode("li", [
                LeafNode(None, "Item "),
                LeafNode("i", "two"),
                LeafNode(None, " with "),
                LeafNode("a", "link", {"href": "url.com"}),
            ]),
        ])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_ol_block_to_html_node_basic(self):
        block = "1. First\n2. Second"
        node = ol_block_to_html_node(block)
        expected_node = ParentNode("ol", [
            ParentNode("li", [LeafNode(None, "First")]),
            ParentNode("li", [LeafNode(None, "Second")]),
        ])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_ol_block_to_html_node_with_inline(self):
        block = "1. Item **one**\n2. Item _two_ with `code`"
        node = ol_block_to_html_node(block)
        expected_node = ParentNode("ol", [
            ParentNode("li", [
                LeafNode(None, "Item "),
                LeafNode("b", "one"),
            ]),
            ParentNode("li", [
                LeafNode(None, "Item "),
                LeafNode("i", "two"),
                LeafNode(None, " with "),
                LeafNode("code", "code"),
            ]),
        ])
        self.assertEqual(node.to_html(), expected_node.to_html())


    def test_paragraph_block_to_html_node_single_line(self):
        block = "This is a simple paragraph."
        node = paragraph_block_to_html_node(block)
        expected_node = ParentNode("p", [LeafNode(None, "This is a simple paragraph.")])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_paragraph_block_to_html_node_multi_line_no_markdown(self):
        block = "This is a paragraph.\nIt spans multiple lines."
        node = paragraph_block_to_html_node(block)
        expected_node = ParentNode("p", [LeafNode(None, "This is a paragraph. It spans multiple lines.")])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_paragraph_block_to_html_node_with_inline_markdown(self):
        block = "A paragraph with **bold** and _italic_ text."
        node = paragraph_block_to_html_node(block)
        expected_node = ParentNode("p", [
            LeafNode(None, "A paragraph with "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " text."),
        ])
        self.assertEqual(node.to_html(), expected_node.to_html())

    def test_markdown_to_html_node_full_document_example(self):
        md = textwrap.dedent("""
            # Heading One

            This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

            ```
            print("Hello, world!")
            def greet(name):
                return f"Hello, {name}!"
            ```

            > This is a quote block.
            > It can span multiple lines.

            - First unordered item
            - Second unordered item

            1. First ordered item
            2. Second ordered item
            3. Third ordered item
        """)
        html_node = markdown_to_html_node(md)        
        expected_html = ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "Heading One")]),
            ParentNode("p", [
                LeafNode(None, "This is a paragraph of text. It has some "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " words inside of it."),
            ]),
            ParentNode("pre", [LeafNode("code", "print(\"Hello, world!\")\ndef greet(name):\n    return f\"Hello, {name}!\"")]),
            ParentNode("blockquote", [
                LeafNode(None, "This is a quote block.\nIt can span multiple lines.")
            ]),
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "First unordered item")]),
                ParentNode("li", [LeafNode(None, "Second unordered item")]),
            ]),
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "First ordered item")]),
                ParentNode("li", [LeafNode(None, "Second ordered item")]),
                ParentNode("li", [LeafNode(None, "Third ordered item")]),
            ]),
        ])
        self.assertEqual(html_node.to_html(), expected_html.to_html())

if __name__ == "__main__":
    unittest.main()
