from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Service.BusinessLogic import Tokens, Security, Services, config
import base64, json

def api(request):
    html=   '<h1>Welcome to our API</h1>' \
            '<h2> In order to create a new user! </h2>' \
            '<ul>'\
                '<li><b>Do a POST request on /api/create/user/token/&lttoken&gt </b><br>' \
                    '- You have to use CreateUser class for needed token</li>'\
                '<li><b>Do a POST request on /api/create/user/ </b><br> ' \
                '- You have to give this json in body: <br> {"username": "", "password": "", "email": "" , "encrypted": "True/False"}</li>' \
            '</ul>' \
            '<h2> In order to authenticate user! </h2>' \
            '<ul>'\
                '<li><b> Do a  POST request on /api/auth/user/token/&lttoken&gt</b><br> ' \
                    '</b>- You have to use AuthUser class for needed token</li>' \
                '<li><b>Do a POST request on /api/auth/user/ </b><br> ' \
                    '- You have to give this json in body: <br>' \
                    '{"username": "", "password": "", "email": "" , "encrypted": "True/False"}</li>'\
            '</ul>' \
            '<p> <br>'\
            '<b>Important!!! </b> In both cases you have to use <br>' \
            'UserIdentity class in order to decode response token</p><br><br>'\

    return HttpResponse(html)

def token(request, token):
    html = 'Token is ok - <br>'
    html += token
    return HttpResponse(html)

''' 
    Create CreateUser token based on json data in the body of POST request
    Just for testing/DEBUGING
'''
# Body : {"username": "", "password": "", "email": ""}
@csrf_exempt
def createToken(request):
    if request.method == 'POST':
        try:
            parameters = json.loads(str(request.body, 'utf-8'))
            username=parameters['username']
            password=parameters['password']
            email=parameters['email']
            print("Create user - \nUsername: \"" + str(username) + "\" Password: \"" + str(password) + "\" email: \"" + str(email) +"\"")
            token = Tokens.CreateUser().create_token(username=username, password=password, email=email)
            response = Tokens.Convert().serializableJSON(token=token)
            return HttpResponse(response, content_type="application/json", status=202)
        except :
            return HttpResponse({"error": "Need to add json", 'code': str(config.TOKENS)}, content_type="application/json", status=200)
    else:
        error = {'error': 'You need to use Post request', 'code': str(config.POST_REQUEST)}
        return HttpResponse(json.dumps(error), content_type="application/json", status=400)


''' 
    Create AuthUser token based on json data in the body of POST request
    Just for testing/DEBUGING
'''
# Body : {"username": "", "password": "", "email": ""}
@csrf_exempt
def authToken(request):
    if request.method == 'POST':
        try:
            parameters = json.loads(str(request.body, 'utf-8'))
            username=parameters['username']
            password=parameters['password']
            email=parameters['email']
            print("Auth user - \nUsername: \"" + str(username) + "\" Password: \"" + str(password) + "\" email: \"" + str(email) +"\"")
            token = Tokens.AuthUser().create_token(username=username, password=password, email=email)
            response = Tokens.Convert().serializableJSON(token=token)
            return HttpResponse(response, content_type="application/json", status=202)
        except :
            return HttpResponse({"error": "Need to add json", 'code': str(config.TOKENS)}, content_type="application/json", status=200)
    else:
        error = {'error': 'You need to use Post request', 'code': str(config.POST_REQUEST)}
        return HttpResponse(json.dumps(error), content_type="application/json", status=400)

#------------------------------------------------
# Post /api/create/user/token/<createUser_token>
@csrf_exempt
def create_user_by_token(request, token):
    if request.method == 'POST':
        try:
            response,responseCode = Services.Authentication().createUserByToken(token)
            return HttpResponse(response, content_type="application/json", status=responseCode)
        except Exception as e:
            print(e)
            error = {'error': 'Failed to create new user' , 'code': ''}
            return HttpResponse(json.dumps(error), content_type="application/json", status=500)
    else:
        error = {'error': 'You need to use Post request' , 'code': str(config.POST_REQUEST)}
        return HttpResponse(json.dumps(error), content_type="application/json", status=400)


# Post /api/create/user
# Body : {"username": "", "password": "", "email": "" , "encrypted": ""}
@csrf_exempt
def create_user_request(request, encrypted=False):
    if request.method == 'POST':
        try:
            parameters = json.loads(str(request.body, 'utf-8'))
            #print("========================================" + str(request.body) + "========================================")

            if parameters['encrypted'] == "True":
                encrypted = True

            if encrypted:
                sec = Security.encryption()
                username = sec.decrypt(parameters['username'])
                password = sec.decrypt(parameters['password'])
                email = sec.decrypt(parameters['email'])
            else:
                username = parameters['username']
                password = parameters['password']
                email = parameters['email']
            #print("User data are valid, Create token")
            response,responseCode = Services.Authentication().createUser(username=username, password=password, email=email)
            return HttpResponse(response, content_type="application/json", status=responseCode)
        except Exception as e:
            print(e)
            error = {'error': 'Failed to create new user', 'code': ''}
            return HttpResponse(json.dumps(error), content_type="application/json", status=500)
    else:
        error = {'error': 'You need to use Post request', 'code': str(config.POST_REQUEST)}
        return HttpResponse(json.dumps(error), content_type="application/json", status=400)


def create(request):
    html='<form action="user/" method="post">' \
         '  <input type="submit" value="Submit">' \
         '</form>'
    return HttpResponse(html, status=200)


#------------------------------------------------
@csrf_exempt
def auth_user_by_token(request, token):
    if request.method == 'POST':
        try:
            sec = Security.encryption()
            decodedToken = Tokens.AuthUser().decode_token(token, 'auth')
            username = sec.decrypt(decodedToken['username'])
            password = sec.decrypt(decodedToken['password'])
            email = sec.decrypt(decodedToken['email'])
            if decodedToken['sub'] == "Auth-user":
                response = Services.Authentication().loginUser(username=username, password=password, email=email)
                return HttpResponse(response, content_type="application/json", status=202)
            error = {'error': 'Wrong Token', 'code': '' }
            return HttpResponse(json.dumps(error), content_type="application/json", status=406)
        except Services.UserDoesNotExists as er:
            print(er)
            error = {'error': 'Username/Password is wrong', 'code': '' }
            return HttpResponse(json.dumps(error), content_type="application/json", status=203)
        except Exception as e:
            print(e)
            error = {'error': 'Invalid token', 'code': ''}
            return HttpResponse(json.dumps(error), content_type="application/json", status=401)
    else:
        error = {'error': 'You need to use Post request', 'code': str(config.POST_REQUEST)}
        return HttpResponse(json.dumps(error), content_type="application/json", status=400)


# Body : {"username": "", "password": "", "email": "" , "encrypted": ""}
@csrf_exempt
def auth_user_request(request, encrypted=False):
    if request.method == 'POST':
        try:
            parameters = json.loads(str(request.body, 'utf-8'))

            if parameters['encrypted'] == "True":
                encrypted = True

            if encrypted:
                sec = Security.encryption()
                username = sec.decrypt(parameters['username'])
                password = sec.decrypt(parameters['password'])
                email = sec.decrypt(parameters['email'])
            else:
                username = parameters['username']
                password = parameters['password']
                email = parameters['email']
            response = Services.Authentication().loginUser(username=username, password=password, email=email)
            return HttpResponse(response, content_type="application/json", status=302)
        except Services.UserDoesNotExists as er:
            print(er)
            error = {'error': 'Username/Password is wrong', 'code': '' }
            return HttpResponse(json.dumps(error), content_type="application/json", status=203)
        except Exception as e:
            print(e)
            error = {'error': 'Failed to authenticate user', 'code': '' }
            return HttpResponse(json.dumps(error), content_type="application/json", status=500)
    else:
        error = {'error': 'You need to use Post request', 'code': str(config.POST_REQUEST)}
        return HttpResponse(json.dumps(error), content_type="application/json", status=400)
