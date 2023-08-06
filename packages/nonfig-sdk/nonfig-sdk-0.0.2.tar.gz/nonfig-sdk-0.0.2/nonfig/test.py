import unittest
from unittest.mock import patch
from nonfig.sdk import Nonfig
from nonfig.constants import BASE_URL


class TestSDK(unittest.TestCase):

    def setUp(self):
        self.default_options = {
            'app_id': "c1e8293f-58be-4c55-9db4-b1c39cbc1dcb",  # Replace with your App ID
            'app_secret': "XuuhXorEZqeRTJjHumGCgnPuZMdQgVvu",  # Replace with your App Secret
            'debug': True,
            'cache_enable': True,
            'cache_ttl': 60
        }

    @unittest.expectedFailure
    @classmethod
    def test_constructor_error(cls):
        options = {}
        Nonfig(options)

    def test_constructor_success(self):
        options = self.default_options
        nonfig = Nonfig(options)
        self.assertEqual(nonfig.app_id, options['app_id'])
        self.assertEqual(nonfig.app_secret, options['app_secret'])
        self.assertEqual(nonfig.debug, options['debug'])
        self.assertEqual(nonfig.cache_enable, options['cache_enable'])
        self.assertEqual(nonfig.cache_ttl, options['cache_ttl'])

    def test_get_headers_method(self):
        options = self.default_options
        nonfig = Nonfig(options)
        headers = nonfig.get_headers()
        expected_agent_value = 'Nonfig/v1 PythonBindings/1.0'
        expected_auth_value = "Bearer {}:{}".format(
            options['app_id'], options['app_secret'])
        expect_content_value = "application/json"
        self.assertEqual(headers['user-agent'], expected_agent_value)
        self.assertEqual(headers['authorization'], expected_auth_value)
        self.assertEqual(headers['content-type'], expect_content_value)

    @patch('nonfig.sdk.requests.get')
    def test_find_by_id_method(self, mock_requests):
        options = self.default_options
        configuration_id = "__fake__"
        expect_url = "{}/configurations/id/{}".format(
            BASE_URL, configuration_id)
        nonfig = Nonfig(options)
        nonfig.find_by_id(configuration_id)

        self.assertEqual(mock_requests.call_count, 1)
        mock_requests.assert_called_with(
            expect_url,
            headers=nonfig.get_headers()
        )

    @patch('nonfig.sdk.requests.get')
    def test_find_by_name_method(self, mock_requests):
        options = self.default_options
        name = "__fake__"
        expect_url = "{}/configurations/name/{}".format(
            BASE_URL, name)
        nonfig = Nonfig(options)
        nonfig.find_by_name(name)

        self.assertEqual(mock_requests.call_count, 1)
        mock_requests.assert_called_with(
            expect_url,
            headers=nonfig.get_headers()
        )

    @patch('nonfig.sdk.requests.get')
    def test_find_by_labels_method(self, mock_requests):
        options = self.default_options
        labels = ["label:test"]
        expect_url = "{}/configurations/labels/{}".format(
            BASE_URL, ",".join(labels))
        nonfig = Nonfig(options)
        nonfig.find_by_labels(labels)

        self.assertEqual(mock_requests.call_count, 1)
        mock_requests.assert_called_with(
            expect_url,
            headers=nonfig.get_headers()
        )


if __name__ == '__main__':
    unittest.main()
