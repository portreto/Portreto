"SK EDIT"

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:     #Meta is used to specify which model will change(In this case User)
        model = User
        fields = ['username','email','password1','password2']