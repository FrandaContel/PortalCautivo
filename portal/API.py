#Documentación inicial del script


import base64
import requests
import json
import random
import secrets
import string
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from datetime import datetime
#Clase 
class Fortigate:
    def __init__(self, ip, vdom, token):
        ipaddr = 'https://' + ip
        

        #URL for the login check
        self.ipad = ipaddr

        # URL definition
        self.api_url = ipaddr + '/api/v2/'
        #Dominio virtual
        self.vdom = vdom
        #Authorization API Token
        self.token = token
        
        self.headers = {'Authorization': self.token}
        self.payload= {}
        
    def Status(self):
        url = self.api_url + f'monitor/system/firmware/'
        self.headers = {
            'Authorization': self.token
        }
        data = []
        try:
            print(url)
            print(self.token)
            response = requests.request("GET", url, headers=self.headers, verify=False)
            response = json.loads(response.text)
            data.append(response['status'])
            data.append(response['results']['current']['platform-id'])
            data.append(response['serial'])
            data.append(response['results']['current']['version'])
            data.append(response['results']['current']['build'])
            print(data)
            return data
        except:
            data.append("500")
            return data

    def Logincheck(self,username,passwd):
        #https://10.10.10.1:39443/logincheck
        url = self.api_url + f'logincheck'
        self.headers = {
            'Authorization': self.token
        }
        try:
            print(url)
            print(self.token)
            response = requests.request("GET", url, headers=self.headers, verify=False)
            return response
        except:
            return response
    
    def GetGroupAll(self):
        url = self.api_url + f'cmdb/user/group/'
        self.headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(httpStatus(response))
        print("Grupos: ")
        for i in range (0,len(response['results'])):
            print(response['results'][i]['name'])
    
    def GetGroupMembers(self,name):
        
        url = self.api_url + f'cmdb/user/group/{name}'
        self.headers = {
            'Authorization': self.token
        }
        nombres = []
        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(httpStatus(response))
        print(response['results'][0]['guest'])
        for i in range (0,len(response['results'][0]['guest'])):
            print(response['results'][0]['guest'][i]['expiration'])
            nombres.append(response['results'][0]['guest'][i]['user-id'])
        print(nombres)
        return nombres

    def CreateGroup(self):
        url = self.api_url + f'cmdb/user/group/'
        self.headers = {
            'Authorization': self.token
        }
        name = input("Ingrese el nombre del grupo: ")
        grouptype = input("Ingrese el tipo del grupo:") #firewall
        payload = {'json':      #Payload en formato de Json, donde se enviarán todos los parámetros que serán efectivos.
                    {
                    'name':  name,
                    'group-type': grouptype,
                    }     
                }
        response = requests.request("POST", url, headers=self.headers, data=repr(payload), verify=False)
        response = json.loads(response.text)
        return print(httpStatus(response))
    
    def EditGroupMembers(self):
        self.GetGroupAll()
        name = input("Ingrese el nombre del grupo a editar: ")
        url = self.api_url + f'cmdb/user/group/{name}'
        miembros = []
        nombres = self.GetGroupMembers(name)
        nombres.append("prueba")
        for i in range (0,len(nombres)):
                miembros.append({"name":nombres[i]})
        self.headers = {
            'Authorization': self.token
        }
        payload = {'json':      #Payload en formato de Json, donde se enviarán todos los parámetros que serán efectivos.
                    {
                    'member':  miembros,
                    }     
                }
        response = requests.request("PUT", url, headers=self.headers, data=repr(payload), verify=False)
        response = json.loads(response.text)
        return print(httpStatus(response))

    def GetGroupMembers(self, group_name):
            url = self.api_url + f'cmdb/user/group/{group_name}'
            members = []

            self.payload = ""
            self.headers = {
            'Authorization': self.token
            }

            response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
            #Convertimos la respuesta a formato json para manejar mejor los datos
            response = json.loads(response.text)
            #Se itera por los elementos de la lista "results", donde cada elemento contiene la informacion de un usuario
            members_info = response['results'][0]['guest'] #Se agregan los nombres de los usuarios a una lista vacia
            for i in range(0, len(members_info)):
                if (members_info[i]['expiration']=='300'):
                    members.append(members_info[i]["user-id"])
            print("lol")
            return members[0]
    
    def AddUserToGroup(self, group, correo):
        url = self.api_url + f'cmdb/user/group/{group}/guest'
        
        self.payload = {'json':
                        {
                        'correo':correo,
                        'password':'fortinet',
                        'expiration':300
                        }
                        }
        self.headers = {
            'Authorization': self.token
            }
        
        response = requests.request("POST", url, headers=self.headers, data=repr(self.payload), verify=False)

    def UserGuestEmail(self, group,user_name):
        url = self.api_url + f'monitor/user/guest/email'
        self.headers = {
            'Authorization': self.token
        }
        user = user_name
        user_group = group #firewall
        payload = {'json':      #Payload en formato de Json, donde se enviarán todos los parámetros que serán efectivos.
                    {
                    'group':  user_group,
                    'guest':[user_name]},
                    }     
                
        response = requests.request("POST", url, headers=self.headers, data=repr(payload), verify=False)
        response = json.loads(response.text)
        return print(httpStatus(response))

    

#Devuelve el status del request http, se puede utilizar para validaciones.

def httpStatus(response):
    http_s = response["http_status"]
    return http_s
