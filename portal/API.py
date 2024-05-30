#Documentación inicial del script


import base64
import requests
import json
import random
import secrets
import string
from requests.packages.urllib3.exceptions import InsecureRequestWarning
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

    #Función para el respaldo del equipo
    def BackUp(self):
        url = self.api_url + 'monitor/system/config/backup?destination=file&scope=global'

        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        #response = json.loads(response.text)
        print('aqui')
        backup = response.content
        return backup

    def Licenses(self):
        url = self.api_url + f'monitor/license/status'
        self.headers = {
                'Authorization': self.token
            }
        data = []
        try:
            print(url)
            response = requests.request("GET", url, headers=self.headers, verify=False)
            response = json.loads(response.text)
            
            data.append(['Firmware','Status:',response['results']['device_os_id']['status'], 'Expira', datetime.fromtimestamp(response['results']['device_os_id']['expires'])])
            data.append(['Antivirus','Status:',response['results']['antivirus']['status'], 'Expira', datetime.fromtimestamp(response['results']['antivirus']['expires'])])
            data.append(['IPS','Status:',response['results']['ips']['status'], 'Expira', datetime.fromtimestamp(response['results']['ips']['expires'])])
            data.append(['AntiSpam','Status:',response['results']['antispam']['status'], 'Expira', datetime.fromtimestamp(response['results']['antispam']['expires'])])
            data.append(['Filtrado Web','Status:',response['results']['web_filtering']['status'], 'Expira', datetime.fromtimestamp(response['results']['web_filtering']['expires'])])
            print(data)
            return data
        except:
            print(response)
            data.append("500")
            return data

    def LoginCheck(self):
        url = self.ipad
        self.headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        return response.status_code

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

    #Devuelve todos los traffic shapers del Sistema
    def TrafficShaperGetAll(self):
        lista = []
        url = self.api_url + f'cmdb/firewall.shaper/traffic-shaper/'
        self.headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        #print(httpStatus(response))
        for i in range(0,len(response['results'])):
            lista.append(response['results'][i]['name'])
        return httpStatus(response),lista

    
    #Devuelve toda la información del traffic shaper especificado    
    def TrafficShaperGet(self,shaper_name):

        url = self.api_url + f'cmdb/firewall.shaper/traffic-shaper/{shaper_name}'
        self.headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        data =[]
        data.append(response['results'][0]['name'])
        data.append(response['results'][0]['guaranteed-bandwidth'])
        data.append(response['results'][0]['maximum-bandwidth'])
        data.append(response['results'][0]['priority'])
        print(data)
        return data


    #Modifica el nombre del trafic shapper, necesita como parametro el nombre actual del traffic shaper (shaper_name) y el nuevo nombre del mismo (new_name)
    def TrafficShaperEditName(self, shaper_name, new_name):
        url = self.api_url + f'cmdb/firewall.shaper/traffic-shaper/{shaper_name}'
        #print (token)
        self.payload ="{\n    \"name\":"+new_name+"}\n}"
        self.headers = {
            'Authorization': self.token
        }
        
        response = requests.request("PUT", url, headers=self.headers, data=self.payload, verify=False)
        print(response.text)

    #Modifica el valor del ancho de banda, necesita el nombre del traffic shaper (shaper_name) y el nuevo valor del ancho de banda (max)
    def TrafficShaperEditMax(self,shaper_name,max_bw):
        url = self.api_url + f'cmdb/firewall.shaper/traffic-shaper/{shaper_name}'
        #print (token)
        self.payload ="{\n    \"maximum-bandwidth\":"+max_bw+"}\n}"
        self.headers = {
            'Authorization': self.token
        }
        
        response = requests.request("PUT", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(response['revision_changed'])
        return max_bw,response['revision_changed']
    
    def TrafficShaperEditG_Bandwidth(self, shaper_name,g_bw):
        url = self.api_url + f'cmdb/firewall.shaper/traffic-shaper/{shaper_name}'
        #print (token)
        self.payload ="{\n    \"maximum-bandwidth\":"+g_bw+"}\n}"
        self.headers = {
            'Authorization': self.token
        }
        
        response = requests.request("PUT", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(response['revision_changed'])
        return g_bw,response['revision_changed']
    
    def TrafficShaperEditG_Bandwidth(self, shaper_name,g_bw):
        url = self.api_url + f'cmdb/firewall.shaper/traffic-shaper/{shaper_name}'
        #print (token)
        self.payload ="{\n    \"guaranteed-bandwidth\":"+g_bw+"}\n}"
        self.headers = {
            'Authorization': self.token
        }
        
        response = requests.request("PUT", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(response['revision_changed'])
        return g_bw,response['revision_changed']
    
    def TrafficShaperEditPriority(self, shaper_name,priority):
        url = self.api_url + f'cmdb/firewall.shaper/traffic-shaper/{shaper_name}'
        #print (token)
        self.payload ="{\n    \"priority\":"+priority+"}\n}"
        self.headers = {
            'Authorization': self.token
        }
        
        response = requests.request("PUT", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(response['revision_changed'])
        return priority,response['revision_changed']
    
    #Crea un nuevo Traffic Shaper
    def TrafficShaperEdit(self, shaper_name, maxbandwidth,g_bandwidth, priority):
        url = self.api_url + f'cmdb/firewall.shaper/traffic-shaper/{shaper_name}'
        self.headers = {
            'Authorization': self.token
            }
        payload = {'json':      #Payload en formato de Json, donde se enviarán todos los parámetros que serán efectivos.
                    {
                    'maximum-bandwidth': maxbandwidth,
                    'guaranteed-bandwidth': g_bandwidth,
                    'priority': priority,
                    }     
                }
        response = requests.request("PUT", url, headers=self.headers, data=repr(payload), verify=False)
        print(response.text)
        return response.text
    #Crea un nuevo Traffic Shaper
    def TrafficShaperCreate(self, name,g_bandwidth, maxbandwidth, priority):
        url = self.api_url + 'cmdb/firewall.shaper/traffic-shaper'
        self.headers = {
            'Authorization': self.token
            }
        payload = {'json':      #Payload en formato de Json, donde se enviarán todos los parámetros que serán efectivos.
                    {
                    'name':  name,
                    'maximum-bandwidth': maxbandwidth,
                    'guaranteed-bandwidth': g_bandwidth,
                    'priority': priority,
                    }     
                }
        response = requests.request("POST", url, headers=self.headers, data=repr(payload), verify=False)
        print(response.text)
        return response.text
    
    #Función que se utiliza para eliminar un Traffic Shaper

    def TrafficShaperDelete(self,name):
        url = self.api_url + f'cmdb/firewall.shaper/traffic-shaper/{name}'
        self.headers = {
            'Authorization': self.token
        }
        response = requests.request("DELETE", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        


    #Devuelve en una lista los nombres de los usuarios locales existentes al momento
    def GetLocalUsers(self):
            url = self.api_url + 'cmdb/user/local'
            
            users = []

            self.payload = ""
            self.headers = {
            'Authorization': self.token
            }

            response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
            #Convertimos la respuesta a formato json para manejar mejor los datos
            response = json.loads(response.text)
            #Se itera por los elementos de la lista "results", donde cada elemento contiene la informacion de un usuario
            for i in range (0,len(response['results'])):
                user = []
                user.append(response['results'][i]['name']) #Se agregan los nombres de los usuarios a una lista vacia
                user.append(response['results'][i]['id'])
                user.append(response['results'][i]['status'])
                user.append(response['results'][i]['email-to'])
                users.append(user)
            return users
    
    #Crea un usuario local con nombre, contraseña e email dados
    def CrearLocalUser(self,name,password,email):
        url = self.api_url + 'cmdb/user/local'
        self.headers = {
            'Authorization': self.token
        }

        self.payload = "{\n  \"name\": \"%s\",\n  \"status\": \"enable\",\n  \"type\": \"password\",\n  \"passwd\": \"%s\",\n  \"two-factor\": \"disable\",\n  \"email-to\": \"%s\",\n}\n\n" % (name, password, email)
        response = requests.request("POST", url, headers=self.headers, data=self.payload, verify=False)
        print(response.text)

    #Crea un usuario local con nombre, contraseña e email dados
    def DeleteLocalUser(self,name):
        url = self.api_url + f'cmdb/user/local/{name}'
        self.headers = {
            'Authorization': self.token
        }
        #Para eliminar solo se requiere el nombre del usuario en cuestión
        response = requests.request("DELETE", url, headers=self.headers, data="", verify=False)
        print(response.text)

    #Funcion para obtener a todos los administradores existentes en el equipo FortiGate
    def GetAllSystemAdmin(self):
        url = self.api_url+'cmdb/system/admin/'
        self.headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(httpStatus(response))
        print("Admins: ")
        for i in range (0,len(response['results'])):
            print(response['results'][i]['name'])

    #Funcion para obtener la información de un admin en específico
    def GetSystemAdmin(self,name):
        url = self.api_url+f'cmdb/system/admin/{name}'
        self.headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(httpStatus(response))
        print(f"Admin: {name}")
        print(response['results'])
    
    #Función para eliminar a un admin en específico
    """Para la eliminación del admin en específico
        se requiere de su nombre para ser ubicado en 
        base de datos del sistema.
    """
    def DelSystemAdmin(self,name):
        url = self.api_url+f'cmdb/system/admin/{name}'
        self.headers = {
            'Authorization': self.token
        }
        response = requests.request("DELETE", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(response)
        if self.httpStatus(response)== 200:
            print(f"El admin: {name} fue eliminado correctamente")

    #Funcion para añadir un admin al sistema 
    def AddSystemAdmin(self, name, password):
        """
        Crea un administrador en el vdom que se le asigne, inicialmente está en "root"

        Parametros
        ----------  
        name: El nombre del admin en el Sistema (type string)
        password: La contraseña del admin en el Sistema (type string)
        profile: Perfil del admin, se puede escoger entre: prof_admin/super_admin (type string)(default prof_admin)
        remote_auth: Autentitcacion remota, se puede escoger entre: enable/disable (type string)(default disable)
            
        Return 

        Retornará 200, si todo está correcto y 4XX si existe algún error.
        """ 
        url = self.api_url + 'cmdb/system/admin/' #Url al cual se conectará la API
        self.headers = {
            'Authorization': self.token #El token de API para la autenticación
        }
        name = str(name)
        password = str(password)
        profile = 'super_admin'
        remote_auth = 'disable'
        #profile: prof_admin/super_admin

        payload = {'json':      #Payload en formato de Json, donde se enviarán todos los parámetros que serán efectivos.
                    {
                    'name':  name,
                    'password': password,
                    'accprofile': profile,
                    'remote-auth':remote_auth,
                     "vdom":[
                            {
                        "name":self.vdom,
                            }
                         ]
                    }     
                }
        response = requests.request("POST", url, headers=self.headers, data=repr(payload), verify=False)
        response = json.loads(response.text)
        return print(httpStatus(response))
        
    #Función para el reinicio del sistema
    def RebootSystem(self):
        url = self.api_url+'monitor/system/os/reboot'
        self.headers = {
            'Authorization': self.token
        }
        self.payload={}
        response = requests.request("POST", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(response)


    
    #Función para la restauraciñon del BackUp del equipo (En proceso)
    def RestoreBackUp(self):
        url = self.api_url + 'monitor/system/config/restore'
        headers = {
            'Authorization': self.token
        }
        """with open("BackUp60D_6.conf",'r')as f:
            data = f.read()"""

        """data_bytes = data.encode('ascii')
        base64_bytes = base64.b64encode(data_bytes)
        base64_m = base64_bytes.decode('ascii')"""

        payload = {'json':      #Payload en formato de Json, donde se enviarán todos los parámetros que serán efectivos.
                    {
                    'source':'upload',
                    'scope':'root',
                    'file_content':base64.b64encode(open("BackUp60D_6.conf", "rb").read1())
                    }     
                }
        response = requests.request("POST", url, headers=headers, data=repr(payload), verify=False)
        print(response)

    #Función para la actualización del equipo (En proceso)
    def FirmwareUpgrade(self):
        url = self.api_url + 'monitor/system/firmware/upgrade'
        headers = {
            'Authorization': self.token
        }
        with open("6.0.16-FGT_60D-v6-build0505-FORTINET.out",'rb')as f:
            data = f.read()

        data_bytes = data
        base64_bytes = base64.standard_b64encode(data_bytes)
        base64_m = base64_bytes.decode('ascii')

        payload = {'json':      #Payload en formato de Json, donde se enviarán todos los parámetros que serán efectivos.
                    {
                    'source':'upload',
                    'file_content':base64.encodebytes(base64_bytes)
                    }     
                }
        response = requests.request("POST", url, headers=headers, data=repr(payload), verify=False)
        print(response)

    #Función para observar los administradores que se encuentran conectados al momento.
    def CurrentAdmins(self):
        url = self.api_url + f'monitor/system/current-admins'

        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)

        for i in range(0,len(response['results'])):
            print(response['results'][i]['id'])
            print(response['results'][i]['admin'])

    #Función para ver los perfiles de EndPoint que existen (Actualmente ninguno)
    def EndPoint_Profile(self):
        url = self.api_url + f'cmdb/endpoint-control/profile'

        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(response['results'])
        """for i in range(0,len(response['results'])):
            print(response['results'][i]['id'])
            print(response['results'][i]['admin'])"""

    #Función para ver los perfiles de Firewall que existen
    def FirewallProfile(self):
        url = self.api_url + f'cmdb/firewall/profile-group'

        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        print(response['results'])

    #Función para las políticas existentes en el Firewall
    def FirewallPolicy(self):
        url = self.api_url + 'cmdb/firewall/policy'

        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        for i in range(0,len(response['results'])):
            print("Id: "+str(response['results'][i]['policyid']))
            print("Nombre de la Politica: "+response['results'][i]['name'])
            print("Source: "+response['results'][i]['srcintf'][0]['name'])
            print("Destination: "+response['results'][i]['dstintf'][0]['name'])
            print("\n")

    #Función para obtener los Id de las políticas existentes en el Firewall (Se usa para la función editar)
    def FirewallPolicyId(self):
        url = self.api_url + 'cmdb/firewall/policy'

        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        for i in range(0,len(response['results'])):
            print("Id: "+str(response['results'][i]['policyid']))
            print("Nombre de la Politica: "+response['results'][i]['name'])

    #Función para editar una política mediante su ID (En proceso), se busca de editar la Source Interface y la Dst Interface
    def FirewallPolicyEdit(self):
        self.FirewallPolicyId()

        id = input("Ingrese el Id de la política a editar: ")
        url = self.api_url + f'cmdb/firewall/policy/{id}'
        self.SystemInterfaces()

        src_interface = input("Inserte interfaz de inicio: ") 
        dst_interface = input("Inserte interfaz de destino: ")

        payload = {'json':      #Payload en formato de Json, donde se enviarán todos los parámetros que serán efectivos.
                    {
                    'policyid':  id,
                    'srcintf': [{'name':src_interface }],
                    'dstintf': [{'name':dst_interface }],
                    
                    }     
                }
        
        response = requests.request("PUT", url, headers=self.headers, data=payload, verify=False)
        response = json.loads(response.text)
        print(response)

    #Función para obtener las interfaces existentes en el Firewall
    def SystemInterfaces(self):
        interfaces = []
        
        url = self.api_url + 'cmdb/system/interface'
        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        response = json.loads(response.text)
        
        for i in range(0,len(response['results'])):
            interface = []
            if 'ip' in response['results'][i]:
                interface.append(response['results'][i]['name'])
                interface.append(response['results'][i]['ip'])
                interface.append(response['results'][i]['status'])
                print("Nombre de Address: "+response['results'][i]['name'])
                print("Dirección IP: "+response['results'][i]['ip'])
                print("\n")
                interfaces.append(interface)
        return interfaces


    #Funcion para generar contraseñas semialeatorias y seguras
    #Se utiliza la libreria String para importar letras, numeros y caracteres especiales
    def CreateSafePwd(self):
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        alphabet = letters + digits + special_chars
        pwd_length = 12 #Se establece el largo de la contraseña a 12 caracteres

        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))
        return pwd

    #Crear usuarios con datos autogenerados. El parametro number indica la cantidad de usuarios a crear.
    def CrearAutoLocalUser(self, number):  
        url = self.api_url + 'cmdb/user/local'
        self.headers = {
            'Authorization': self.token
        }
        #Se trae la lista de nombres de usuarios existentes.
        existing_users = self.GetLocalUsers() 
        #Se genera un nombre de usuario con el formato "user"+numero aleatorio
        for i in range(number):
            num = random.randint(0,100000)
            username = "user"+str(num)

            #Verifica que el nombre de usuario generado no exista entre los usuarios ya creados.
            for i in range(len(existing_users)):
                if username == existing_users[i]:
                    while username == existing_users[i]:
                        num = random.randint(0,100000)
                        username = "user"+str(num)

            #Se genera clave segura
            password = self.CreateSafePwd()

            self.payload = "{\n  \"name\": \"%s\",\n  \"status\": \"enable\",\n  \"type\": \"password\",\n  \"passwd\": \"%s\",\n  \"two-factor\": \"disable\",\n}\n\n" % (username, password)
            response = requests.request("POST", url, headers=self.headers, data=self.payload, verify=False)
            print("Usuario creado con exito:\nUsername: "+username+"\nPassword: "+password)
            #Se guardan los datos de los usuarios creados en un archivo .txt
            f= open("localusers_info.txt","a+")  
            f.write("\n \nUsername: "+username+"\nPassword: "+password)
    

#Devuelve el status del request http, se puede utilizar para validaciones.

def httpStatus(response):
    http_s = response["http_status"]
    return http_s
