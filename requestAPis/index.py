# reference link: https://www.datacamp.com/tutorial/making-http-requests-in-python

import requests


def RequestBasic():
    # The API endpoint
    url = "https://jsonplaceholder.typicode.com/posts/1"

    # A GET request to the API
    response = requests.get(url)

    # Print the response
    response_json = response.json()
    print(response_json)

#expected output:
"""
{'userId': 1, 'id': 1, 'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit', 'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'}
"""