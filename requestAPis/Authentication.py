import requests
from requests.auth import HTTPBasicAuth


def RequestGetByAuthen():
    private_url = "https://api.github.com/user"
    github_username = "username"
    token = "token"

    private_url_response = requests.get(
        url = private_url,
        auth = HTTPBasicAuth(github_username, token)
    )

    private_url_response.status_code

#expected output:
"""
200
"""