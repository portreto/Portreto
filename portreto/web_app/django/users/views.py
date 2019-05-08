from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm  #This generates an form contained in the backend of django
from django.contrib import messages #This is the way to show messages success, failure etc
from .forms import UserRegistrationForm #Access form created in forms.py
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':    #Here we specify what we wish to do with our form.We show a message on success
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save() #save the new user created. In the background hashes password
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been successfully created {username}')
            return redirect('portreto-home')    #This is used to redirect in our home page after successful update of form
    else:

        form = UserRegistrationForm()
    return render(request,'users/register.html',{'form': form}) #Again create a template file again to access everything we want

#We will specify something that it is different in each user
@login_required     #@ declarator adds extra functionality on an extisting function
def profile(request):
    return render(request,'users/profile.html')