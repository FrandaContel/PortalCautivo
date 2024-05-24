from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .API import Fortigate 
# Create your views here.
post = None
magic = None
def inicio(request):
    print("Probando")
    data=request.GET
    print(data)
    print("por aquí")
    if (data):
        magic = request.GET['magic']
        post = request.GET['post']
        request.session["magic"] = magic
        request.session["post"] = post
        print(request.session["magic"])
        print(request.session["post"])
    else:
        magic = request.session["magic"]
        post = request.session["post"]
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
    """url = "https://10.10.10.1:39443/"

    payload = "username=admin&secretkey=#5C0ntel6&ajax=1"
    headers = {
    'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    print(response.text)
    print("registro")
    Usuario: apitest
    Token API: f7m6mmbhpG9fjgmbh0h763hznH1h0Q
    Por si acaso: f7m6mmbhpG9fjgmbh0h763hznH1h0Q
    """
    
    if request.method=="GET":
        print("Se obtiene para la creación del usuario Guest")
        return render(request,"registro_guest.html")
    else:
        data=request.POST
        correo = data['correo']
        print(correo)
        ip = "10.10.10.1"
        port = "39443"  
        vdom = "root"
        token = 'Bearer '+'f7m6mmbhpG9fjgmbh0h763hznH1h0Q'
        fg = Fortigate(f'{ip}:{port}', vdom, token) 
        fg.Status()
        user_group = "GuestPiramides"
        fg.AddUserToGroup(user_group,correo)
        fg.GetGroupMembers(user_group)


        return redirect("/portal")

def login(request):
    print("login")