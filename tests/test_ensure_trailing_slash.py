import unittest
from broken_links.broken_links import ensure_trailing_slash

class TestEnsureTrailingSlash(unittest.TestCase):

    def test_ensure_trailing_slash(self):
        self.assertEqual(ensure_trailing_slash("http://example.com/path/to/resource"), "http://example.com/path/to/resource/")
        self.assertEqual(ensure_trailing_slash("http://example.com/path/to/resource.html"), "http://example.com/path/to/resource.html")
        self.assertEqual(ensure_trailing_slash("http://example.com/path/to/resource?query=param"), "http://example.com/path/to/resource/?query=param")
        self.assertEqual(ensure_trailing_slash("http://example.com/path/to/resource#fragment"), "http://example.com/path/to/resource/#fragment")
        self.assertEqual(ensure_trailing_slash("http://example.com/path/to/resource.html?query=param"), "http://example.com/path/to/resource.html?query=param")
        self.assertEqual(ensure_trailing_slash("http://example.com/path/to/resource.html#fragment"), "http://example.com/path/to/resource.html#fragment")

if __name__ == '__main__':
    unittest.main()
