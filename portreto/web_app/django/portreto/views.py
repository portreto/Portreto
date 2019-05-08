"""
SK EDIT
Views handle what is going to happen on each response
"""
from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def home(request):
    #return HttpResponse('<h1>HOME</h1>') #Always return pass a request as parameter
    return render(request, 'portreto/home.html') #render is used to load the templates that we wish to render on each case.Returns an Httprequest.Third argument is used to pass data

def about(request):
    return render(request, 'portreto/about.html') #render is used to load the templates that we wish to render on each case.Returns an Httprequest
