import requests
from http import HTTPStatus
class fetch_api_data:

    def __init__(self, token):
        self.token = token
        self.data = None

    def fetch_data(self, url, request_type="GET", data=None):
        headers =  {"Authorization": f"Bearer {self.token}"}
        if request_type == "GET":
            response = requests.get(url, headers=headers)
        elif request_type == "POST":
            response = requests.post(url, headers=headers, data=data)
        elif request_type == "PUT":
            response = requests.put(url, headers=headers, data=data)
        elif request_type == "DELETE":
            response = requests.delete(url, headers=headers)
    
        if response.status_code == HTTPStatus.OK:
            self.data = response.json()
            return self.data
