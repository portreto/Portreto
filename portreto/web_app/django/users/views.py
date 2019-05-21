from django.shortcuts import render,redirect , get_object_or_404
#from django.contrib.auth.forms import UserCreationForm  #This generates an form contained in the backend of django
from django.contrib import messages #This is the way to show messages success, failure etc
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm #Access form created in forms.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from webmain.models import Gallery
from webmain.views import is_friend

# Create your views here.


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
    user = request.user
    my_galleries = Gallery.objects.filter(GalleryOwner=user).all()
    if request.method == 'POST':

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)    #request.files for images

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
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
    #value = request.POST.get('uname', None)
    #profile = Profile.objects.get(user=user_id)
    user = get_object_or_404(User, username=username)

    my_galleries = {}

    if is_friend(request,user.id):
        my_galleries = Gallery.objects.filter(GalleryOwner=user)

    # return redirect('/' + str(instance.username))

    # if request.method == 'POST':
    #
    #     user_form = UserUpdateForm(request.POST, instance=request.user)
    #     profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)    #request.files for images
    #
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #         messages.success(request, f'Your account has been successfully updated')
    #         return redirect('users:profile')
    # else:

    user_form = UserUpdateForm(instance=user)
    profile_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'user': user,
        'user_form': user_form,
        'profile_form' : profile_form,
        'my_galleries': my_galleries,
    }
    return render(request,'users/profile.html',context)
    #return redirect('users:profile')
