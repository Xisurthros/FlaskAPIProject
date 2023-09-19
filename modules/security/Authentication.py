import os
import hashlib
from flask import jsonify


def invalidAPIKeyError() -> jsonify:
    return {"status": 500, "error": "Invalid API key"}


class Authentication:
    """
    The user will be authenticated by providing an API key.

    Each API key should be unique to each user.
    The API keys should be stored in a separate database.
    For the sake of this project, I will be using a static API key.
    """

    def __init__(self):
        self.saved_api_token = os.environ.get("API_KEY")
        self.sha256_api_token_converted = lambda api_key: hashlib.sha256(api_key.encode()).hexdigest()

    def check_api_key(self, api_key: str) -> bool:
        """
        Table names are case seem to be set to all lower case base on my testing with requests specifically
        Convert all keys in a dict to lowercase

        :param api_key: api key to be checked
        :return: True if the api key is valid, False if the api key is invalid
        """

        return self.saved_api_token == self.sha256_api_token_converted(api_key)
