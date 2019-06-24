from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from . import Tokens, Security, config
import base64,json
from jwt import DecodeError, InvalidSignatureError

class UserAlreadyExists(Exception):
    pass

class UserDoesNotExists(Exception):
    pass


class Authentication:
    def __init__(self):
        pass

    def createUserByToken(self, token, permissions=['read','write']):
        try:
            sec = Security.encryption()
            decodedToken = Tokens.CreateUser().decode_token(token, 'auth')
            username = sec.decrypt(decodedToken['username'])
            password = sec.decrypt(decodedToken['password'])
            email = sec.decrypt(decodedToken['email'])
            admin = decodedToken['admin']

            if (decodedToken['create-user'] == True and decodedToken['sub'] ==  "Create-new-user"):
                return self.createUser(username,password,email,admin,permissions)
            else:
                return json.dumps({'error': 'Create new user request is not available', 'code': ''}), 406
        except Exception as e:
            print(e)
            return json.dumps({'error': 'Invalid token', 'code': ''}), 401

    def createUser(self, username, password, email, admin=False, permissions=['read','write']):
        try:
            uid = self.createUserInDatabase(username, password, email, admin, permissions)
            responseToken = Tokens.UserIdentity().create_token(
                username=username,
                email=email,
                uid=uid,
                newUser=True,
                admin=admin,
                permissions=permissions
            )
            return Tokens.Convert().serializableJSON(responseToken), 201
        except UserAlreadyExists as ae:
            print(ae)
            return json.dumps({'error': 'User already exists', 'code': ''}), 400
        except Exception as e:
            print(e)
            return json.dumps({'error': 'Creation of new user token failed', 'code': ''}), 500


    # TODO
    def createUserInDatabase(self, username, password, email, admin=False, permissions=['read','write']):
        try:
            newUser = User(
                username=str(username),
                email=email,
                is_superuser=admin,
                # permissions=permissions
            )

            newUser.set_password(str(password))
            newUser.save()
            return newUser.pk
        except :
            raise UserAlreadyExists("Username is taken")


    def loginUser(self, username, password, email):
        user = authenticate(username=username, password=password)
        if user is not None:
            responseToken = Tokens.UserIdentity().create_token(
                username=User.objects.get(pk=user.pk).username,
                email=User.objects.get(pk=user.pk).email,
                uid=user.pk,
                newUser=False,
                admin=User.objects.get(pk=user.pk).is_superuser,
            )
            return Tokens.Convert().serializableJSON(responseToken)
        else:
            raise UserDoesNotExists("User does not exist")


class Application:
    def __init__(self):
        pass

class Storage:
    def __init__(self):
        pass

class Web:
    def __init__(self):
        pass
