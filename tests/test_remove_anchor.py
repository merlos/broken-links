import unittest
from broken_links.broken_links import remove_anchor

class TestRemoveAnchor(unittest.TestCase):

    def test_remove_anchor(self):
        self.assertEqual(remove_anchor("http://whatever.whatever.com/whatever.html#remove-anchor"), "http://whatever.whatever.com/whatever.html")
        self.assertEqual(remove_anchor("http://whatever.whatever.com/whatever.html"), "http://whatever.whatever.com/whatever.html")
        self.assertEqual(remove_anchor("http://whatever.whatever.com/whatever.html?query=param#remove-anchor"), "http://whatever.whatever.com/whatever.html?query=param")
        self.assertEqual(remove_anchor("http://whatever.whatever.com/whatever.html?query=param"), "http://whatever.whatever.com/whatever.html?query=param")
        self.assertEqual(remove_anchor("https://whatever.whatever.com/whatever.html#remove-anchor"), "https://whatever.whatever.com/whatever.html")
        self.assertEqual(remove_anchor("ftp://whatever.whatever.com/whatever.html#remove-anchor"), "ftp://whatever.whatever.com/whatever.html")
        self.assertEqual(remove_anchor("http://whatever.whatever.com/#remove-anchor"), "http://whatever.whatever.com/")
        self.assertEqual(remove_anchor("http://whatever.whatever.com/#"), "http://whatever.whatever.com/")
        self.assertEqual(remove_anchor("http://whatever.whatever.com/"), "http://whatever.whatever.com/")

if __name__ == '__main__':
    unittest.main()
