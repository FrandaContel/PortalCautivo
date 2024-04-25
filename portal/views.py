from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
post = None
magic = None
def inicio(request):
    print("Probando")
    data=request.GET
    magic = request.GET['magic']
    post = request.GET['post']
    print(magic)
    print(post)
    if request.method=="GET":
        print("Iniciando sesión")
        return render(request,"login.html",{ 
            'magic':magic,
            'post':post,
            })
    else:
        print("Listo")
    




def registro(request):
    url = "https://10.10.10.1:39443/"

    payload = "username=admin&secretkey=#5C0ntel6&ajax=1"
    headers = {
    'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    print(response.text)
    print("registro")


def login(request):
    print("login")