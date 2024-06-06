from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .API import Fortigate 
# Create your views here.
post = None
magic = None

def connect(request):
    ip = "10.10.10.1"
    port = "39443"  
    vdom = "root"
    token = 'Bearer '+'f7m6mmbhpG9fjgmbh0h763hznH1h0Q'
    fg = Fortigate(f'{ip}:{port}', vdom, token) 
    fg.Status()
    user_group = "GuestPortalCaptive"
    fg.AddUserToGroup(user_group,'algo@gmail.com')
    test = fg.GetGroupMembers(user_group)

    if request.method=="GET":
        magic = request.GET['magic']
        post = request.GET['post']
        usuario = test
        passwd = 'fortinet'
        print("Se obtiene conexión directa")
        return render(request,"auth.html",{ 
                'magic':magic,
                'post':post,
                'username':usuario,
                'passwd':passwd
                })
