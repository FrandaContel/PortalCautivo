from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .API import Fortigate 
# Create your views here.
post = None
magic = None

def connect(request):
    print("Probando")
    data=request.GET
    print(data)
    print("por aquí")
    ip = "10.10.10.1"
    port = "39443"  
    vdom = "root"
    token = 'Bearer '+'f7m6mmbhpG9fjgmbh0h763hznH1h0Q'
    fg = Fortigate(f'{ip}:{port}', vdom, token) 
    fg.Status()
    user_group = "GuestPiramides"
    fg.AddUserToGroup(user_group,'algo@gmail.com')
    test = fg.GetGroupMembers(user_group)
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
        usuario = test
        passwd = 'fortinet'
        print("Se obtiene conexión directa")
        return render(request,"auth.html",{ 
                'magic':magic,
                'post':post,
                'username':usuario,
                'passwd':passwd
                })

"""https://10.10.45.1:1003/fgtauth/csrfmiddlewaretoken=3rFLJci9xQh4fUOE3yLm0tJ0wvaWSWJ1&magic=070f0889e5fdd1ed&username=prueba_contel&password=123456789"""