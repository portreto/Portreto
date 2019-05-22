"SK EDIT"

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from webmain.models import Profile

import requests, json
DEBUG = True

AUTH_DOMAIN_NAME = 'auth'
AUTH_PORT = '8000'

APP_DOMAIN_NAME = 'app'
APP_PORT = '8000'

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:     #Meta is used to specify which model will change(In this case User)
        model = User
        fields = ['username','email','password1','password2']

    def save(self, commit=True):
        try:
            if DEBUG is True: print("=" * 40 + "\nRegister Data:")
            # TODO : Change domain and port based on online Auth server
            protocol = 'http://'
            domain = AUTH_DOMAIN_NAME  # '127.0.0.1'
            port = AUTH_PORT
            location = '/api/create/user/'
            url = str(protocol) + str(domain) + ':' + str(port) + str(location)
            if DEBUG is True: print(url)
            data = {
                "username": str(self.cleaned_data["username"]),
                "password": str(self.cleaned_data["password1"]),
                "email": str(self.cleaned_data["email"]),
                "encrypted": "False"
            }
            if DEBUG is True: print(data)
            response = requests.post(url=url, data=json.dumps(data))
            if DEBUG is True: print(response.status_code)
            if DEBUG is True: print(json.loads(str(response.text)))
            if DEBUG is True: print("~" * 40)
            # Operation completed
            if response.status_code == 201:
                return "DONE", json.loads(str(response.text))
            # User already exists
            elif response.status_code == 400:
                return json.loads(str(response.text))["error"], 0
            # Internal Server Error (Error codes = 404, 500, 401, 406)
            else:
                return "Unexpected error. Please try again later!", 0

        except Exception as e:
            print("++++++++++++++++++++++++++++++++++++++++++++++\n" + str(
                e) + "\n++++++++++++++++++++++++++++++++++++++++++++++")
            return "Internal Server error. Please try again later", 0



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:     #Meta is used to specify which model will change(In this case User)
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['FirstName','LastName','Bio','Sex','BirthDate','ProfilePhoto']