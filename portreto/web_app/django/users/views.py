from django.shortcuts import render,redirect , get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from webmain import api_client
from django.http import Http404


from .UserConnection import *
from django.http import HttpResponse

LOGIN = "users:login"
REGISTER = "users:register"
PORTRETO = "webmain:index"
AUTH_DOMAIN_NAME = 'auth'
AUTH_PORT = '8000'

APP_DOMAIN_NAME = 'app'
APP_PORT = '8000'


# Create your views here.
def get_api_objects_or_404(objects):

    if len(objects) == 0:
        raise Http404('No matches the given query.')
    return objects

def register(request):
    token = my_cookie_get(request, TOKEN_COOKIE)
    username = my_cookie_get(request, USERNAME_COOKIE)
    #User is already logged in
    if token is not None and username is not None:
        return redirect(PORTRETO)  # TODO : change path add parameters ?next=next_page

    if request.method == 'POST':    #Here we specify what we wish to do with our form.We show a message on success
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            message, data = form.save()
            if DEBUG is True: print()
            if message == "DONE" :    #save the new user created. In the background hashes password

                # TODO:
                # Send token for the first time to Application Service in order to create user
                protocol = 'http://'
                domain = AUTH_DOMAIN_NAME  # '127.0.0.1'
                port = AUTH_PORT
                location = '/api/create/user/'
                url = str(protocol) + str(domain) + ':' + str(port) + str(location)
                #response = requests.post(url=url, data=data["token"])

                # TODO: POST THIS USERNAME TO APP LOGIC
                username = form.cleaned_data.get('username')
                messages.success(request,f'Your account has been successfully created {username}')

                user = User(username=username)
                api_client.post_user(user,username)

                response = redirect(PORTRETO)    #This is used to redirect in our home page after successful update of form
                my_cookie_set(response, TOKEN_COOKIE, data["token"])

                return my_cookie_set(response,
                                     USERNAME_COOKIE,
                                     encryption().decrypt(UserIdentity().decode_token( data["token"], "app")["username"]))
            elif message == 400:
                messages.error(request, message)
                return render(request, 'register/', {'form': form})
            else:
                messages.error(request, message)
                return render(request,'users/register.html', {'form': form})
    else:

        form = UserRegistrationForm()
    return render(request,'users/register.html', {'form': form}) #Again create a template file again to access everything we want

def login(request, next=None):
    token = my_cookie_get(request, TOKEN_COOKIE)
    username = my_cookie_get(request, USERNAME_COOKIE)
    #User is already logged in
    if token is not None and username is not None:
        return redirect(PORTRETO)  # TODO : change path add parameters ?next=next_page

    if request.method == 'POST':

        form = AuthenticationForm(request= request, data = request.POST)
        if form.is_valid():
            pass
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        message, data = auth_user(username=username, password=password)

        if message == "DONE":
            if DEBUG is True: print("Hello, " + encryption().decrypt(UserIdentity().decode_token(data["token"], "app")["username"]))

            response = redirect(PORTRETO)
            my_cookie_set(response, TOKEN_COOKIE, data["token"])

            return my_cookie_set(response,
                                 USERNAME_COOKIE,
                                 encryption().decrypt(UserIdentity().decode_token(data["token"], "app")["username"]))
        elif message == 203:
            messages.error(request, data)
            return render(request, 'users/login.html', {'form': form})
        else:
            messages.error(request, message)
            return render(request, 'users/login.html', {'form': form})

    else:
        form = AuthenticationForm()
    return render(request,'users/login.html', {'form': form}) #Again create a template file again to access everything we want

def logout(request):
    return logout_user(request)

@my_login_required()
def profile(request, username=None, token=None):
    requsername = username
    user = get_api_objects_or_404(api_client.get_user(username=requsername))[0]
    profile = get_api_objects_or_404(api_client.get_profile(username=requsername))[0]


    my_galleries = api_client.get_gallery(requsername=requsername,username=requsername)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)    #request.files for images

        if user_form.is_valid() and profile_form.is_valid():
            tuser = user_form.save(commit=False)
            tprofile = profile_form.save(commit=False)

            api_client.put_user(tuser,requsername)
            api_client.put_profile(tprofile,requsername)

            messages.success(request, f'Your account has been successfully updated')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user': user,
        'profile' : profile,
        'user_form': user_form,
        'profile_form' : profile_form,
        'my_galleries': my_galleries,
        'requsername' : requsername
    }
    return render(request,'users/profile.html',context)

#TODO ADD CHECKS
@my_login_required()
def getProfile(request, profile_username, username=None, token=None):
    requsername = username

    user = get_api_objects_or_404(api_client.get_user(username=profile_username))[0]

    profile = get_api_objects_or_404(api_client.get_profile(username=profile_username))[0]

    my_galleries = api_client.get_gallery(requsername=requsername, username=profile_username)

    user_form = UserUpdateForm(instance=user)
    profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user': user,
        'profile' : profile,
        'user_form': user_form,
        'profile_form' : profile_form,
        'my_galleries': my_galleries,
        'requsername' : requsername
    }
    return render(request,'users/profile.html',context)
    #return redirect('users:profile')
