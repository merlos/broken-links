import unittest
from link_checker.link_checker import should_ignore

class TestShouldIgnore(unittest.TestCase):

    def test_should_ignore_exact_match(self):
        patterns = ['http://example.com/ignore-this-page']
        self.assertTrue(should_ignore('http://example.com/ignore-this-page', patterns))
        self.assertFalse(should_ignore('http://example.com/another-page', patterns))

    def test_should_ignore_prefix_match(self):
        patterns = ['http://example.com/ignore/*']
        self.assertTrue(should_ignore('http://example.com/ignore/anything', patterns))
        self.assertFalse(should_ignore('http://example.com/not-ignore/anything', patterns))

    def test_should_ignore_suffix_match(self):
        patterns = ['*/ignore-this-path/*']
        self.assertTrue(should_ignore('http://example.com/ignore-this-path/anything', patterns))
        self.assertFalse(should_ignore('http://example.com/not-ignore-this-path/anything', patterns))

    def test_should_ignore_subdomain_match(self):
        patterns = ['https://*.domain.com']
        self.assertTrue(should_ignore('https://sub.domain.com', patterns))
        self.assertFalse(should_ignore('https://domain.com', patterns))
        self.assertTrue(should_ignore('https://another.sub.domain.com', patterns))
        self.assertFalse(should_ignore('https://sub.domain.com/subpath', patterns))

    def test_should_ignore_subdomain_with_path_match(self):
        patterns = ['https://*.domain.com*']
        self.assertTrue(should_ignore('https://sub.domain.com', patterns))
        self.assertTrue(should_ignore('https://sub.domain.com/subpath', patterns))
        self.assertFalse(should_ignore('https://domain.com', patterns))
        self.assertTrue(should_ignore('https://another.sub.domain.com', patterns))

    def test_should_ignore_no_match(self):
        patterns = ['http://example.com/ignore-this-page']
        self.assertFalse(should_ignore('http://example.com/another-page', patterns))
        self.assertFalse(should_ignore('http://example.com/ignore-this-page/extra', patterns))

if __name__ == '__main__':
    unittest.main()
