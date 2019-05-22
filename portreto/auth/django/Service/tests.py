from django.test import TestCase
from django.http import HttpRequest

# Create your tests here.

import json, requests
from Service.BusinessLogic.Tokens import CreateUser
s= requests.post(url="http://127.0.0.1:8000/api/create/token",json=json.dumps({"username":"user102","password":"password102","email":"user102@email.com","encrypted":"False"}))


class test:
    def __init__(self):
        self.cleaned_data={"username":"username1","password":"password1","email":"email1",}

    def save(self, commit=True):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        email = self.cleaned_data["email"]
        token = CreateUser().create_token(username=username, password=password, email=email)

        # TODO : Change domain and port
        protocol = 'http://'
        domain = '127.0.0.1'
        port = '8000'
        location = '/api/create/user/token/'
        url = str(protocol) + str(domain) + ':' + str(port) + str(location) + str(token, 'utf-8') + '/'

        print("========================\nPost request on:\n" + str(url) + "\n========================")
        data = {"username": "user21", "password": "pass21", "email": "email21", }

        response = requests.post(url, json=json.dumps(data), )
        print(response)

        if True:  # response.status_code == 201:
            # TODO : Create COOKIE
            return True
        else:
            return False


