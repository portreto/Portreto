
import datetime
from functools import wraps

import requests,json
from django.shortcuts import redirect

from .BusinessLogic.Security import encryption
from .BusinessLogic.Tokens import UserIdentity


# ==================== IMPORTANT =====================

PROTOCOL_VALID = True

TOKEN_COOKIE = "portreto-auth-token"
USERNAME_COOKIE = "portreto-user-username"

AUTH_DOMAIN_NAME = 'auth'
AUTH_PORT = '8000'

APP_DOMAIN_NAME = 'app'
APP_PORT = '8001'

COOKIES_EXPIRE_AFTER = 30

BASIC_URL = '127.0.0.1:8001/' if PROTOCOL_VALID is False else "http//127.0.0.1:8001/"
LOGIN_PAGE = "users:login"

DEBUG= True
# ====================================================


def my_cookie_set(response, field, data):
    response.set_cookie(
        field,
        str(data),
        expires=datetime.datetime.utcnow() + datetime.timedelta(days=COOKIES_EXPIRE_AFTER, seconds=0),
        httponly=True,
        path="/",
    )
    return response


def my_cookie_get(request, field):
    if field in request.COOKIES:
        return request.COOKIES[field]
    else:
        return


def delete_my_cookies(response):
    response.delete_cookie(TOKEN_COOKIE)
    response.delete_cookie(USERNAME_COOKIE)
    return response


def cookie_in_blacklist(token, domainIn=None, portIn=None):
    protocol='' if PROTOCOL_VALID is False else 'http://'
    domain = APP_DOMAIN_NAME if domainIn is None else domainIn
    port = APP_PORT if portIn is None else portIn
    location = '/delete/token/'
    url = str(protocol) + str(domain) + ':' + str(port) + str(location)
    data = {"token": token}

    try:
        response = requests.post(url, data=json.dumps(data))
        if response.status_code == 202:
            return True
        else:
            return
    except:
        return True # TODO

# ------------------------------------------------------------------------


def login_user():
    pass


def logout_user(request):
    if DEBUG is True: print("=" * 40 + "\nLogout User:")
    if cookie_in_blacklist(token= request.COOKIES[TOKEN_COOKIE]) is not None:
        if DEBUG is True: print("BlackList request and Delete Cookies")
        response = redirect('users:login')
        response.delete_cookie(TOKEN_COOKIE)
        response.delete_cookie(USERNAME_COOKIE)
        if DEBUG is True: print("~" * 40)
        return response
    else:
        if DEBUG is True: print("BlackList request FAILED")
        if DEBUG is True: print("~" * 40)
        return redirect("webmain:index")


def auth_user(username="", password=""):
    try:
        print("=" * 40 + "\nLogin")
        protocol = 'http://'
        domain = AUTH_DOMAIN_NAME
        port = AUTH_PORT
        location = '/api/auth/user/'
        url = str(protocol) + str(domain) + ':' + str(port) + str(location)
        if DEBUG is True: print(url)

        data = {
            'username': str(username),
            'password': str(password),
            'email': '',
            'encrypted': 'False'
        }
        if DEBUG is True: print(data)

        response = requests.post(url=url, data= json.dumps(data))
        if DEBUG is True:print(response.status_code)
        if DEBUG is True:print("~" * 40)

        # Operation completed (Found)
        if response.status_code == 302:
            return "DONE", json.loads(str(response.text))
        # Username/Password is wrong
        elif response.status_code == 203:
            return 203, json.loads(str(response.text))["error"]
        # Internal Server Error (Error codes = 400,500)
        else:
            return "Unexpected error. Please try again later!", 0
    except Exception as e:
        if DEBUG is True:print (e)
        return "Internal Server error. Please try again later",0



def my_login_required(login_page= None, next_page= None):
    def decorator(function= None):
        @wraps(function)
        def wrapper(request, username= None, token= None, *args , **kwargs):
            if DEBUG is True: print("=" * 40 + "\nLogin_required:")
            login_url = LOGIN_PAGE if login_page is None else login_page
            next = '' if next_page is None else "?next=" + next_page
            redirect_url = login_url + next

            # Check cookie
            token = my_cookie_get(request, TOKEN_COOKIE)
            username = my_cookie_get(request, USERNAME_COOKIE)
            if token is None or username is None:
                # login page in case there is not valid cookie
                response = redirect(login_url) #
                if token is not None:
                    cookie_in_blacklist(token)
                if DEBUG is True: print("One or both of the cookies is/are missing\n"+"~" * 40)
                return delete_my_cookies(response)
            else:
                try:
                    if username == encryption().decrypt(UserIdentity().decode_token(token,"app")["username"]):
                        if DEBUG is True: print("Both of the cookies are ok\n"+"~" * 40)
                        return function(request, *args , **kwargs, username=username, token=token)
                    else:
                        cookie_in_blacklist(token)
                        response = redirect(login_url)
                        if DEBUG is True: print("One of the cookies is not valid\n"+"~""~" * 40)
                        return delete_my_cookies(response)
                except Exception as e:
                    cookie_in_blacklist(token)
                    response = redirect(login_url)
                    if DEBUG is True: print("Internal Server error\n"+"~" * 40)
                    return delete_my_cookies(response)
        return wrapper
    return decorator

