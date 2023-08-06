"""Integrate Nonfig using SDK"""
import requests
from nonfig.constants import BASE_URL


class Nonfig:
    """Initialize API instance to fetch data from Nonfig"""
    base_url = BASE_URL
    api_url = "{}/configurations".format(base_url)

    def __init__(self, options: dict):
        self.app_id = options['app_id']
        self.app_secret = options['app_secret']
        self.debug = options['debug'] or False
        self.cache_enable = options['cache_enable'] or False
        self.cache_ttl = options['cache_ttl']

    def get_headers(self):
        """Retrieve HTTP Headers for the API Request"""
        return {
            'user-agent': "Nonfig/v1 PythonBindings/1.0",
            'authorization': "Bearer {}:{}".format(self.app_id, self.app_secret),
            'content-type': 'application/json'
        }

    def find_by_id(self, configuration_id: str) -> dict:
        """Fetch a Configuration by it's Unique ID

        Keyword arguments:
        configuration_id -- UUID of the configuration
        """
        headers = self.get_headers()
        full_url = '{}/id/{}'.format(self.api_url, configuration_id)
        request = requests.get(full_url, headers=headers)

        return request.json()

    def find_by_name(self, name: str):
        """Fetch a Configuration by fully qualified name

        Keyword arguments:
        name -- Name of the configuration (incl. Path if any)
        """
        headers = self.get_headers()
        full_url = '{}/name/{}'.format(self.api_url, name)
        request = requests.get(full_url, headers=headers)

        return request.json()

    def find_by_path(self, path: str) -> list:
        """Fetch a list of Configurations by path

        Keyword arguments:
        path -- High-level path (i.g directory-like path)
        """
        headers = self.get_headers()
        full_url = '{}/path/{}'.format(self.api_url, path)
        request = requests.get(full_url, headers=headers)

        return request.json()

    def find_by_labels(self, labels: list) -> list:
        """Fetch a list of Configurations by path

        Keyword arguments:
        path -- High-level path (i.g directory-like path)
        """
        headers = self.get_headers()
        full_url = '{}/labels/{}'.format(self.api_url, ','.join(labels))
        request = requests.get(full_url, headers=headers)

        return request.json()
