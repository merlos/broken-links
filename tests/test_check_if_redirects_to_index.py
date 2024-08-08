import unittest
import requests
from unittest.mock import patch, Mock
from broken_links.broken_links import check_if_redirects_to_index

class TestCheckIfRedirectsToIndex(unittest.TestCase):

    @patch('requests.head')
    def test_redirects_to_index(self, mock_head):
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {'Location': 'https://unicef.github.io/magasin/mag-cli/mag_superset/index.html'}
        mock_head.return_value = mock_response

        url = "https://unicef.github.io/magasin/mag-cli/mag_superset"
        self.assertTrue(check_if_redirects_to_index(url))

    @patch('requests.head')
    def test_does_not_redirect(self, mock_head):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response

        url = "https://unicef.github.io/magasin/mag-cli/mag_superset"
        self.assertFalse(check_if_redirects_to_index(url))

    @patch('requests.head')
    def test_redirects_to_non_index(self, mock_head):
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {'Location': 'https://unicef.github.io/magasin/mag-cli/mag_superset/other.html'}
        mock_head.return_value = mock_response

        url = "https://unicef.github.io/magasin/mag-cli/mag_superset"
        self.assertFalse(check_if_redirects_to_index(url))

    @patch('requests.head')
    def test_no_location_header(self, mock_head):
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {}
        mock_head.return_value = mock_response

        url = "https://unicef.github.io/magasin/mag-cli/mag_superset"
        self.assertFalse(check_if_redirects_to_index(url))

    @patch('requests.head')
    def test_request_exception(self, mock_head):
        mock_head.side_effect = requests.RequestException

        url = "https://unicef.github.io/magasin/mag-cli/mag_superset"
        self.assertFalse(check_if_redirects_to_index(url))

if __name__ == '__main__':
    unittest.main()
