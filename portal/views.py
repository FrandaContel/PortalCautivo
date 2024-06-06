from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .API import Fortigate 
from .models import mac_users
# Create your views here.
post = None
magic = None

def connect(request):
    ip = "10.10.10.1"
    port = "39443"  
    vdom = "root"
    token = 'Bearer '+'f7m6mmbhpG9fjgmbh0h763hznH1h0Q'
    

    if request.method=="GET":

        usermac = request.GET['usermac']
        print(usermac)
        magic = request.GET['magic']
        post = request.GET['post']
        try:
            value = mac_users.objects.filter(macaddrs__icontains=usermac)
            value = value.__len__()
            print(value)
        except Exception as e:
            value = 0
            print(e)
            print("volvi por aca")
        if (value <=2):
            mac_users.objects.create(macaddrs= usermac)
            fg = Fortigate(f'{ip}:{port}', vdom, token) 
            fg.Status()
            user_group = "GuestPortalCaptive"
            #fg.AddUserToGroup(user_group,'algo@gmail.com')
            test = fg.GetGroupMembers(user_group)
            usuario = test
            passwd = 'fortinet'
            print("Se obtiene conexión directa")
            return render(request,"auth.html",{ 
                    'magic':magic,
                    'post':post,
                    'username':usuario,
                    'passwd':passwd
                    })
        else: 
            return render (request,'mac-noauth.html')
