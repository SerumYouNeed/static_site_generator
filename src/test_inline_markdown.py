import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    extract_markdown_images,
    text_to_textnodes,
    extract_title
)

class TestInlineMarkdown(unittest.TestCase):
    def test_split_node_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "`", text_type_code), [
                            TextNode("This is text with a ", text_type_text),
                            TextNode("code block", text_type_code),
                            TextNode(" word", text_type_text),
                            ])

    def test_split_bold_del(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "**", text_type_bold), [
                            TextNode("This is text with a ", text_type_text),
                            TextNode("bold block", text_type_bold),
                            TextNode(" word", text_type_text),
                            ])    
        
    def test_split_italic_del(self):
        node = TextNode("This is text with a *italic block* word", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "*", text_type_italic), [
                            TextNode("This is text with a ", text_type_text),
                            TextNode("italic block", text_type_italic),
                            TextNode(" word", text_type_text),
                            ])    
        
    def test_split_del_infront(self):
        node = TextNode("*italic block* in front", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "*", text_type_italic), [
                            TextNode("italic block", text_type_italic),
                            TextNode(" in front", text_type_text),
                            ])    
        
    def test_split_many_dels(self):
        node = TextNode("*italic block* in front and *italic block* in the middle and on the *back*", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "*", text_type_italic), [
                            TextNode("italic block", text_type_italic),
                            TextNode(" in front and ", text_type_text),
                            TextNode("italic block", text_type_italic),
                            TextNode(" in the middle and on the ", text_type_text),
                            TextNode("back", text_type_italic)
                            ])
         
    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])   

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ], 
        textnodes
    )
     
    def test_extract_title_normal(self):
        text = "# Hello"
        positive = "Hello"
        extracted = extract_title(text)
        self.assertEqual(extracted, positive)

    def test_extract_title_left_space(self):
        text = "#         Hello"
        positive = "Hello"
        extracted = extract_title(text)
        self.assertEqual(extracted, positive)

    def test_extract_title_right_space(self):
        text = "# Hello                    "
        positive = "Hello"
        extracted = extract_title(text)
        self.assertEqual(extracted, positive)
        
if __name__ == "__main__":
    unittest.main()