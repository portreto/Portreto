from rest_framework.utils import json
from .BusinessLogic.Tokens import UserIdentity, encryption
from django.contrib.auth.models import User
from app_service.settings import DEBUG


def token_check(get_response):
    # This middleware is responsible for making sure every request is accompanied by the appropriate JWT token
    # and creates a new user if the aforementioned is for a user which does not already exist in the database
    # The token is checked for expiration date and compared to a blacklist
    def print_debug(message, data=None):
        if not DEBUG: return
        string = "\n\n" + "=" * 160 + '\n' + message + '\n'
        if data is not None:
            string += str(data) +'\n'
        string+= "="*160
        print(string)



    def middleware(request):
        print_debug("REQUEST",request)
        print_debug("REQUEST BODY",request.body)

        # Get token from header
        token = request.META.get("HTTP_TOKEN")
        print_debug("REQUEST TOKEN",token)


        # Decode and validate token
        identity = UserIdentity()
        decoded_token = identity.decode_token(token, 'app')
        print_debug("REQUEST DECODED TOKEN",decoded_token)

        # Decrypt Username and Email
        crypt = encryption()
        username = crypt.decrypt(decoded_token['username'])
        email = crypt.decrypt(decoded_token['email'])
        print_debug("REQUEST USERNAME, EMAIL",username+' '+email)

        # If such user does not exist, create new user
        obj, created = User.objects.update_or_create(username=username,defaults={'email':email})

        if not User.objects.filter(username = username).exists():
            print_debug("CREATING NEW USER")
            newuser = User(username=username,email=email)
            newuser.save()


        response = get_response(request)
        return response

    return middleware