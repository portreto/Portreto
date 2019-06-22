from django.shortcuts import render
# Create your views here.
from .models import Gallery
from django.http import HttpResponse

import socket
HOSTNAME = socket.gethostname()

# index page
def index(request):
    HOSTNAME = socket.gethostname()
    responce = "<H1>Application Service</H1>" + \
               "<P> Hostname: " + HOSTNAME + "</P>"

    return HttpResponse(responce)
