from django.test import TestCase
from django.http import HttpResponse
from Service.BusinessLogic import Tokens
from Service.BusinessLogic import Security
import json

def test(request):
    return HttpResponse(test_case())



def test_case():
    html = '<h1>User Ident Test Screen</h1>'

    try:
        cu = Tokens.StoragePermission()
        token = cu.create_token()
        response= cu.toJSON(token)
        html +="<pre>" + str(token) + "</pre><br>"
        html += "<script> var mytext = JSON.stringify(" + str(response) + ",null,4) </script>"
        html += '<p><span id="demo"></span></p>'
        html += '<script>document.getElementById("demo").innerHTML = mytext</script>'
        en = Security.encryption()
        html+= '<p>' + str(en.decrypt(response.get('payload').get('username'))) + '</p>'
    except Exception as e:
        html += "<p>Token failed: <br>" + e + "</p>"
        print("---------TOKEN FAILED---------")

    return html