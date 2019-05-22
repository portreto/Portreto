import jwt
import datetime
import json
import base64
from Crypto.Hash.SHA256 import hashlib

## Custom
from .Security import encryption
from . import config
import json


'''
    Use this class in order to create JSON responses
    based on created tokens
'''
class Convert:
    def __init__(self):
        pass

    def toJSON(self, token, pad='=='):
        try:
            header, payload, signature = str(token).split('.')
            payload = json.loads(str(base64.b64decode(str(payload) + pad), 'UTF-8'))
            response = {
                "payload": payload,
                "token": str(token,'UTF-8'),
            }
            return response
        except Exception as e:
            return e

    def serializableJSON(self, token, pad="=="):
        try:
            return json.dumps(self.toJSON(token=token, pad=pad))
        except Exception as e:
            return e



'''
    Use this Class only when you want to create a new user 

    Encode new user token during his/hers signup
        on Web Service 

    Decode token only on Authentication Service,
        on every new user creation request in order to act stateless
'''
class CreateUser:
    def __init__(self):
        self.iss = "Web-Service"
        self.sub = "Create-new-user" 
        self.aud = config.AUTHENTICATION_SERVICE

    def decode_token(self, token, aud):
        try:
            if isinstance(token, str):
                token = bytes(token,'UTF-8')

            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                audience=aud,
                algorithm='HS256'
            )
            return payload
        except jwt.InvalidAudience as ia:
            return ia
        except jwt.ExpiredSignatureError as es:
            return es
        except Exception as e:
            raise Exception("Failed to decode new user creation token!" + e)

    def create_token(self, username='username', password='password', email='user@portreto.com', create_user=True, admin=False, actions=None):
        en = encryption()
        now = datetime.datetime.utcnow()
        tid = str(config.SALT) + str(self.iss) + str(self.sub) + str(self.aud) + str(now) + str(username) + str(email)

        try:
            payload = {
                'iss': self.iss,
                'sub': self.sub,
                'aud': self.aud,
                'exp': now + datetime.timedelta(days=config.CREATE_USER_TOKEN_EXPIRE_AFTER, seconds=0),
                'nbf': now,
                'iat': now,
                'username': en.encrypt(username),
                'password': en.encrypt(password),
                'email': en.encrypt(email),
                'token-id': str(base64.b64encode(hashlib.sha256(tid.encode('utf-8')).digest()),'utf-8'),
                'create-user': create_user,
                'admin': admin,
                'extra-actions': actions,
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            raise Exception("Failed to Create new user creation token!" + e)

'''
    Use this Class only when you want to authenticate user 

    Encode user token during his/hers login
        on Web Service 

    Decode token only on Authentication Service,
        on every user login request in order to act stateless
'''
class AuthUser:
    def __init__(self):
        self.iss = "Web-Service"
        self.sub = "Auth-user"
        self.aud = config.AUTHENTICATION_SERVICE

    def decode_token(self, token, aud):
        try:
            if isinstance(token, str):
                token = bytes(token,'UTF-8')

            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                audience=aud,
                algorithm='HS256'
            )
            return payload
        except jwt.InvalidAudience as ia:
            return ia
        except jwt.ExpiredSignatureError as es:
            return es
        except Exception as e:
            raise Exception("Failed to decode user auth token!" + e)

    def create_token(self, username='username', password='password', email='user@portreto.com', actions=None):
        en = encryption()
        now = datetime.datetime.utcnow()
        tid = str(config.SALT) + str(self.iss) + str(self.sub) + str(self.aud) + str(now) + str(username) + str(email)

        try:
            payload = {
                'iss': self.iss,
                'sub': self.sub,
                'aud': self.aud,
                'exp': now + datetime.timedelta(days=config.LOGIN_TOKEN_EXPIRE_AFTER, seconds=0),
                'nbf': now,
                'iat': now,
                'username': en.encrypt(username),
                'password': en.encrypt(password),
                'email': en.encrypt(email),
                'token-id': str(base64.b64encode(hashlib.sha256(tid.encode('utf-8')).digest()),'utf-8'),
                'extra-actions': actions,
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            raise Exception("Failed to Create user auth token!" + e)




'''
    Use this Class only for Authentication Purposes

    Encode token for a user during his/hers login or signup
        on Authentication Service 

    Decode tokens only on Application Service,
        on every user request in order to act stateless
'''


class UserIdentity:
    def __init__(self):
        self.iss = "Authentication-Service"
        self.sub = "User-Ident-Token"
        self.aud = config.APPLICATION_SERVICE

    def decode_token(self, token, aud):
        try:
            if isinstance(token, str):
                token = bytes(token,'UTF-8')

            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                audience=aud,
                algorithm='HS256'
            )
            return payload
        except jwt.InvalidAudience as ia:
            return ia
        except jwt.ExpiredSignatureError as es:
            return es
        except Exception as e:
            raise Exception("Failed to authenticate user!" + e)

    def create_token(self, username='username', email='user@portreto.com', uid='user-1', newUser=False, admin=False, permissions=None, actions=None):
        en = encryption()
        now = datetime.datetime.utcnow()
        tid = str(config.SALT) + str(self.iss) + str(self.sub) + str(self.aud) + str(now) + str(username) + str(email)

        try:
            payload = {
                'iss': self.iss,
                'sub': self.sub,
                'aud': self.aud,
                'exp': now + datetime.timedelta(days=config.USER_ID_TOKEN_EXPIRE_AFTER, seconds=0),
                'nbf': now,
                'iat': now,
                'username': en.encrypt(username),
                'email': en.encrypt(email),
                'uid': en.encrypt(uid),
                'userIsNew': newUser,
                'token-id': str(base64.b64encode(hashlib.sha256(tid.encode('utf-8')).digest()),'utf-8'),
                'admin': admin,
                'permissions': permissions,
                'extra-actions': actions,
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            raise Exception("Failed to Create Authentication token!" + e)




'''
    Use this Class only when you want to retrieve files from Storage Services 

    Encode new user token during his/hers action request 
        on Application Service 

    Decode token only on Storage Service,
        on every new user file request in order to act stateless
'''
class StoragePermission:
    def __init__(self):
        self.iss = "Application-Service"
        self.sub = "File-Permission" 
        self.aud = config.STORAGE_SERVICE

    def decode_token(self, token, aud):
        try:

            if isinstance(token, str):
                token = bytes(token,'UTF-8')

            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                audience=aud,
                algorithm='HS256'
            )
            return payload
        except jwt.InvalidAudience as ia:
            return ia
        except jwt.ExpiredSignatureError as es:
            return es
        except Exception as e:
            raise Exception("Failed to authenticate user permission on this file!" + e)

    def create_token(self, username='username', email='user@portreto.com', uid='user-1', url='portreto/image', fileID='img-1', fileName='portreto', actions=None):
        en = encryption()
        now = datetime.datetime.utcnow()
        tid = str(config.SALT) + str(self.iss) + str(self.sub) + str(self.aud) + str(now) + str(username) + str(email)

        try:
            payload = {
                'iss': self.iss,
                'sub': self.sub,
                'aud': self.aud,
                'exp': now + datetime.timedelta(days=config.STORAGE_TOKEN_EXPIRE_AFTER, seconds=0),
                'nbf': now,
                'iat': now,
                'username': en.encrypt(username),
                'email': en.encrypt(email),
                'uid': en.encrypt(uid),
                'url': url,
                'file-ID': fileID,
                'file-Name': fileName,
                'token-id': str(base64.b64encode(hashlib.sha256(tid.encode('utf-8')).digest()),'utf-8'),
                'extra-actions': actions,
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            raise Exception("Failed to create user permission token!" + e)
