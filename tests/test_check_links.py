import requests
import unittest
from unittest.mock import patch
from broken_links.broken_links import check_link

class TestCheckLinks(unittest.TestCase):

    @patch('requests.head')
    def test_check_link_success(self, mock_head):
        mock_head.return_value.status_code = 200
        self.assertTrue(check_link('http://example.com'))

    @patch('requests.head')
    def test_check_link_failure(self, mock_head):
        mock_head.return_value.status_code = 404
        self.assertFalse(check_link('http://example.com'))

    @patch('requests.head')
    def test_check_link_exception(self, mock_head):
        mock_head.side_effect = requests.RequestException
        self.assertFalse(check_link('http://example.com'))

if __name__ == '__main__':
    unittest.main()
