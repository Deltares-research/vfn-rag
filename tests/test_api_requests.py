import unittest
from unittest.mock import patch, Mock
from voice_for_nature_backend.api_requests import make_request


class TestMakeRequest(unittest.TestCase):

    url = "https://api.ebird.org/v2/data/obs/region/recent"
    headers = {"Authorization": "Bearer fake_token"}

    @patch("requests.get")
    def test_success(self, mock_get):
        # Mock the response object and its behavior for a successful request
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"observations": ["bird1", "bird2"]}
        mock_get.return_value = mock_response

        # Call the function
        result = make_request(self.url, self.headers)

        # Assert that the result matches the mocked JSON response
        self.assertEqual(result, {"observations": ["bird1", "bird2"]})
        mock_get.assert_called_once_with(self.url, headers=self.headers)

    @patch("requests.get")
    def test_failure(self, mock_get):
        # Mock the response object for a failed request (e.g., 404 error)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Capture the printed output during the error
        with self.assertLogs(level="INFO") as log:
            result = make_request(self.url, self.headers)

        # Assert that the function returns None in case of failure
        self.assertIsNone(result)
        # Check that the error message is printed
        self.assertIn("Error: Unable to fetch data (status code 404)", log.output[-1])
        mock_get.assert_called_once_with(self.url, headers=self.headers)
