import unittest
from link_checker.link_checker import load_ignore_patterns
import os

class TestLoadIgnorePatterns(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_ignore_file.txt'
        with open(self.test_file, 'w') as f:
            f.write('http://example.com/ignore-this-page\n')
            f.write('http://example.com/ignore/*\n')
            f.write('*/ignore-this-path/*\n')
            f.write('https://*.domain.com\n')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_ignore_patterns(self):
        patterns = load_ignore_patterns(self.test_file)
        self.assertEqual(len(patterns), 4)
        self.assertIn('http://example.com/ignore-this-page', patterns)
        self.assertIn('http://example.com/ignore/*', patterns)
        self.assertIn('*/ignore-this-path/*', patterns)
        self.assertIn('https://*.domain.com', patterns)

    def test_load_ignore_patterns_file_not_exist(self):
        patterns = load_ignore_patterns('non_existent_file.txt')
        self.assertEqual(patterns, [])

if __name__ == '__main__':
    unittest.main()
