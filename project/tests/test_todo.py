# Mock APIs data: https://realpython.com/testing-third-party-apis-with-mocks/
# Third-party imports...
from nose.tools import assert_true
import requests

from api_routes import TODO_LIST


def test_request_response():
    # Send a request to the API server and store the response.
    response = requests.get(TODO_LIST)

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)