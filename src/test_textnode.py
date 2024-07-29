import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_tx_noteq(self):
        node = TextNode("lorem ipsum", "bold")
        node2 = TextNode("inny ipsum", "bold")
        self.assertNotEqual(node, node2)

    def test_type_noteq(self):
        node = TextNode("lorem ipsum", "bold")
        node2 = TextNode("lorem ipsum", "italic")
        self.assertNotEqual(node, node2)
  
    def test_nourl(self):
        node = TextNode("lorem ipsum", "bold")
        if node.url == None:
            msg = "URL value is None."
            self.assertIsNone(node.url, msg)
        
    def test_eq_url(self):
        node = TextNode("lorem ipsum", "bold", "https://www.google.com")
        node2 = TextNode("lorem ipsum", "bold", "https://www.google.com")
        self.assertEqual(node, node2)
        


if __name__ == "__main__":
    unittest.main()