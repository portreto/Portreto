from rest_framework.utils import json
from .BusinessLogic.Tokens import UserIdentity, encryption
from django.contrib.auth.models import User


def token_check(get_response):
    # This middleware is responsible for making sure every request is accompanied by the appropriate JWT token
    # and creates a new user if the aforementioned is for a user which does not already exist in the database
    # The token is checked for expiration date and compared to a blacklist

    def middleware(request):
        # Get token from http +
        print("\n\n" + "=" * 160 + "\nREQUEST \n" + str(request) + "\n" + "=" * 160)
        print("\n\n" + "=" * 160 + "\nREQUEST BODY\n" + str(request.body) + "\n" + "=" * 160)
        token = request.META.get("HTTP_TOKEN")
        # Decode and validate token
        print("\n\n" + "=" * 160 + "\nREQUEST TOKEN\n" + str(token) + "\n" + "=" * 160)

        identity = UserIdentity()
        decoded_token = identity.decode_token(token, 'app')
        print("\n\n" + "=" * 160 + "\nREQUEST DECODED TOKEN\n" + str(decoded_token) + "\n" + "=" * 160)
        # Decrypt Username and Email
        crypt = encryption()
        username = crypt.decrypt(decoded_token['username'])
        email = crypt.decrypt(decoded_token['email'])
        print("\n\n" + "=" * 160 + "\nREQUEST USERNAME:\n" + str(username) + "EMAIL :" + str(email) +"\n"+  "=" * 160)

        # If such user does not exist, create new user
        if not User.objects.filter(username = username).exists():
            print("\n\n" + "=" * 160 + "\nCREATING NEW USER\n" + "=" * 160)
            newuser = User(username=username,email=email)
            newuser.save()


        response = get_response(request)
        return response

    return middleware