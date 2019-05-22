from django.shortcuts import render,redirect , get_object_or_404
#from django.contrib.auth.forms import UserCreationForm  #This generates an form contained in the backend of django
from django.contrib import messages #This is the way to show messages success, failure etc
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm #Access form created in forms.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from webmain.models import Gallery
from webmain.views import is_friend
from webmain import api_client
from django.http import Http404


# Create your views here.
def get_api_objects_or_404(objects):

    if len(objects) == 0:
        raise Http404('No matches the given query.')
    return objects


def register(request):
    if request.method == 'POST':    #Here we specify what we wish to do with our form.We show a message on success
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save() #save the new user created. In the background hashes password
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been successfully created {username}')
            return redirect('webmain:index')    #This is used to redirect in our home page after successful update of form
    else:

        form = UserRegistrationForm()
    return render(request,'users/register.html', {'form': form}) #Again create a template file again to access everything we want

#We will specify something that it is different in each user
@login_required(login_url='users:login')     #@ declarator adds extra functionality on an extisting function
def profile(request):
    requsername = request.user.username

    user = get_api_objects_or_404(api_client.get_user(username=requsername))[0]
    profile = get_api_objects_or_404(api_client.get_profile(username=requsername))[0]


    my_galleries = api_client.get_gallery(requsername=requsername,username=requsername)

    if request.method == 'POST':

        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)    #request.files for images

        if user_form.is_valid() and profile_form.is_valid():
            tuser = user_form.save(commit=False)
            tprofile = profile_form.save(commit=False)

            api_client.post_user(tuser,requsername)
            api_client.post_profile(tprofile,requsername)

            messages.success(request, f'Your account has been successfully updated')
            return redirect('users:profile')
    else:

        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user': user,
        'user_form': user_form,
        'profile_form': profile_form,
        'my_galleries': my_galleries,
    }
    return render(request,'users/profile.html',context)

#TODO ADD CHECKS
@login_required(login_url='users:login')
def getProfile(request,username):
    requsername = request.user.username

    user = get_api_objects_or_404(api_client.get_user(username=username))[0]

    profile = get_api_objects_or_404(api_client.get_profile(username=username))[0]

    my_galleries = api_client.get_gallery(requsername=requsername,username=username)

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
