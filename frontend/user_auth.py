import requests
AUTH_URL = "http://127.0.0.1:8080/login/"
class userAuth:
    def __init__(self, user_name, Password):

        self.user_name = user_name
        self.Password = Password
        self.token = None
   
    def login(self):
        auth_token = requests.post(AUTH_URL, data={"username": self.user_name, "password": self.Password})

        if auth_token.status_code == 200:
            self.token = auth_token.json()["access_token"]
            return self.token
        
    def signup(self, email):
        pass

    