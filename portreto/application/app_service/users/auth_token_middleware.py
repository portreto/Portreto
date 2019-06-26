from django.http import HttpResponse
from rest_framework import status
from rest_framework.utils import json
from .BusinessLogic.Tokens import UserIdentity, encryption
from django.contrib.auth.models import User
from webmain.models import Profile
from .models import TokenBlacklist
# from app_service.settings import DEBUG


def token_check(get_response):
    '''
    This middleware is responsible for making sure every request is accompanied by the appropriate JWT access token
    and creates a new user if the aforementioned is for a user which does not already exist in the database
    The token is checked for expiration date and compared to a blacklist
    :param get_response:
    :return: response
    '''
    DEBUG = True

    def print_debug(message, data=None):
        if not DEBUG: return
        string = "\n\n" + "=" * 160 + '\n' + message + '\n'
        if data is not None:
            string += str(data) +'\n'
        string+= "="*160
        print(string)


    def middleware(request):

        # Create admin profile if non exists
        if User.objects.filter(username='admin').exists():
            admin = User.objects.get(username='admin')
            frofile, created = Profile.objects.get_or_create(user=admin)


        print_debug("REQUEST",request)
        print_debug("REQUEST BODY",request.body)
        print_debug("REQUEST META",request.META)


        if DEBUG and '/admin' in str(request):
            response = get_response(request)
            return response

        try:
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

            # Check if token in blacklist
            token_id = decoded_token['token-id']
            if TokenBlacklist.objects.filter(token_id=token_id).exists():
                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

            # If such user does not exist, create new user
            # obj, created = User.objects.update_or_create(username=username,defaults={'email':email})
            if not User.objects.filter(username = username).exists():
                print_debug("CREATING NEW USER")
                newuser = User(username=username,email=email)
                newuser.save()

            response = get_response(request)
            return response
        except:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    return middleware