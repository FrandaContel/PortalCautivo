from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
import requests
from .API import Fortigate 
from .models import mac_users
# Create your views here.
post = None
magic = None

def connect(request):
    ip = "10.220.252.1"
    port = "39443"  
    vdom = "F1K8SRVBL_P"
    token = 'Bearer '+'fwN8jcG3gN65Gk8jH1nGd5fjxr753N'
    #
    #xcq9dq7nbg6spxfcgdy3z3rmHc7bjq Nuevo user API (contel)
    #f7m6mmbhpG9fjgmbh0h763hznH1h0Q Viejo user API (viejo con muchos permisos)
    if request.method=="GET":
        usermac = request.GET['usermac']
        request.session['usermac'] = usermac
        magic = request.GET['magic']
        request.session['magic']=magic
        post = request.GET['post']
        request.session['post'] = post
        try:
            value = mac_users.objects.filter(macaddrs__icontains=usermac,hora__gte=timezone.now().replace(hour=0, minute=0, second=0), hora__lte=timezone.now().replace(hour=23, minute=59, second=59))
            value = value.__len__()
            print(value)
        except Exception as e:
            value = 0
            print(e)
        if (value <=2):
            fg = Fortigate(f'{ip}:{port}', vdom, token) 
            fg.Status()
            user_group = "GuestPortalCaptive"
            fg.AddUserToGroup(user_group,'algo@gmail.com')
            test = fg.GetGroupMembers(user_group)
            usuario = test
            passwd = 'fortinet'
            return render(request,"auth.html",{ 
                    'magic':magic,
                    'post':post,
                    'username':usuario,
                    'passwd':passwd
                    })
        else: 
            return render (request,'mac-noauth.html')

def redirect(request):
    print("bnc")
    usermac = request.session['usermac']
    print(usermac)
    mac_users.objects.create(macaddrs=usermac)
    print("Redireccionando...")
    return render(request,'redirect.html')

