from ezdnac.excepts import *
import requests
import json
import re
import os

authToken = None
timeout = None
verifySSL = False
baseurl = '/api/v1/'
authbaseurl = '/api/system/v1/'


class DnaC():
    def __init__(self, ip, uid, pw=None, **kwargs):
        global timeout
        global authToken
        self.ip = ip
        self.uid = uid
        self.pw = pw

        # Setting possible keyword adguments:
        try:
            self.port = kwargs['port']
        except KeyError:
            self.port = "443"

        try:
            self.verifySSL = False
            verifySSL = kwargs['verifySSL']
        except KeyError:
            self.verifySSL = False
            verifySSL = False
        try:
            self.authToken = kwargs['authToken']
            authToken = kwargs['authToken']
        except:
            pass

        if timeout is None:
            try:
                timeout = kwargs['timeout']
                self.timeout = timeout
            except KeyError:
                timeout = 5
                self.timeout = timeout
            else:
                pass

        if authToken is None:
            #Authenticate and retreive an authToken
            AuthURL = "https://" + self.ip + ":" + self.port + authbaseurl + "auth/token"
            headers = {}
            try:
                print("Authenticating...")
                response = requests.request("POST", AuthURL, headers=headers, verify=verifySSL, auth=(self.uid, self.pw), timeout=timeout)
            except:
                print("Error: Timeout connection to DNA-C. Most likely a network reachability issue")
                exit()
            data = json.loads(response.text)
            if 'error' in data:
                print (data['error'])
                exit()
            else:
                print ("Login Success")
            authToken = (data['Token'])    
            self.authToken = authToken
        else:
            #print ("Reusing existing key..")
            self.authToken = authToken


    def taskStatus(self, **kwargs):
        try:
            self.taskId = kwargs['id']
        except:
            pass

        if self.taskId == None:
            raise ezDNACError('No previous task to check')
        
        url = "https://" + self.ip + ":" + self.port + "/api/v1/task/" + self.taskId
        payload = {}
        headers = {
        'x-auth-token': self.authToken,
        'Content-Type': 'application/json',
        }
        response = requests.request("GET", url, headers=headers, json=payload, verify=verifySSL, timeout=timeout)
        data = json.loads(response.text)
        return data['response']
        



    #Get the selected device ID from serial:
    def getAllDevices(self):
        url = "https://" + self.ip + ":" + self.port + baseurl + "network-device/"
        payload = {}
        headers = {
        'x-auth-token': self.authToken
        }
        response = requests.request("GET", url, headers=headers, data = payload, verify=verifySSL, timeout=timeout)
        data = json.loads(response.text)    
        return data

    def id_from_serial(self, serialNumber):
        switches = self.getAllDevices()
        for switch in switches['response']:
            if switch['serialNumber'] == serialNumber:
                switchId = switch['id']
        try:
            return switchId
        except KeyError:
            return None


    def getTemplates(self):
        url = "https://" + self.ip + ":" + self.port + baseurl + "template-programmer/project"
        payload = {}
        headers = {
        'x-auth-token': self.authToken
        }
        response = requests.request("GET", url, headers=headers, data = payload, verify=verifySSL, timeout=timeout)
        data = json.loads(response.text)
        
        return data

    def getTemplateId(self, templateName):
        data = self.getTemplates()
        for projects in data:
            for templates in projects['templates']:
                try:
                    if templates['name'] == templateName:
                        return (templates['id'])
                except:
                    return None

    def getTemplateInfo(self, templateId):
        url = "https://" + self.ip + ":" + self.port + baseurl + "template-programmer/template/" + templateId
        headers = {
            'x-auth-token': self.authToken
        }
        response = requests.get(url, headers=headers, verify=verifySSL, timeout=timeout)
        data = json.loads(response.text)
        
        return data

    def getSites(self, **kwargs):
        try:
            searchsite=kwargs['site']
        except:
            searchsite=None
        if searchsite == None:
            url = "https://" + self.ip + ":" + self.port + "/dna/intent/api/v1/site"
        else:
            url = "https://" + self.ip + ":" + self.port + "/dna/intent/api/v1/site?name=" + searchsite + ""
        
        payload = {}
        headers = {
        'x-auth-token': self.authToken,
        'Content-Type': 'application/json',
        '__runsync': 'true',
        '__timeout': '10',
        '__persistbapioutput': 'true',
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=verifySSL, timeout=timeout)
        data = json.loads(response.text)

        if searchsite != None:        
            for site in data['response']:
                return site['id']

        return data['response']
        


    def getPnpDevices(self, **kwargs):
        try:
            serialNumber = kwargs['sn']
        except:
            serialNumber = None
        url = "https://" + self.ip + ":" + self.port + "/dna/intent/api/v1/onboarding/pnp-device?state=Unclaimed"
        payload = {}
        headers = {
        'x-auth-token': self.authToken
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=verifySSL, timeout=timeout)
        data = json.loads(response.text)

        if serialNumber == None:
            return data
        else:
            for device in data:
                if serialNumber in device['deviceInfo']['serialNumber']:
                    ret = device
            try:
                return device
            except:
                raise ezDNACError('Device with serial number' + serialNumber + ' not found in pnp.')



    def getInventoryDevies(self, **kwargs):
        try:
            serialNumber = kwargs['sn']
        except:
            serialNumber = None
        try:
            deviceId = kwargs['id']
        except:
            deviceId = None

        if deviceId != None:
            url = "https://" + self.ip + ":" + self.port + baseurl + "network-device/" + deviceId
        else:
            url = "https://" + self.ip + ":" + self.port + baseurl + "network-device/"

        payload = {}
        headers = {
        'x-auth-token': self.authToken
        }
        response = requests.request("GET", url, headers=headers, data = payload, verify=verifySSL, timeout=timeout)
        data = json.loads(response.text)    
        
        if deviceId != None:
            return data['response']
        else:
            if serialNumber == None:
                return data['response']
            else:
                for device in data['response']:
                    if serialNumber in device['serialNumber']:
                        return device


    def pullTemplates(self, **kwargs):
        path = ""
        projectName = None
        try:
            projectName = kwargs['project']
        except:
            pass
        try:
            path = kwargs['path']
        except:
            pass

        url = "https://" + self.ip + ":" + self.port + baseurl + "template-programmer/project"
        headers = {
          'x-auth-token': self.authToken,
          'Content-Type': 'application/json',
        }
        response = requests.request("GET", url, headers=headers, verify=verifySSL)
        data = json.loads(response.text)
        templateslist = []
        #Get the id of interesting templates:
        for projects in data:
            if projectName != None:
                if (projects['name']) == projectName:
                    for template in projects['templates']:
                        templates = {}
                        templates['id'] = template['id']
                        templateslist.append(templates)
            else:
                for template in projects['templates']:
                    templates = {}
                    templates['id'] = template['id']
                    templateslist.append(templates)
                
        for template in templateslist:
            url = "https://" + self.ip + ":" + self.port + baseurl + "template-programmer/template/"+template['id']
            headers = {
              'x-auth-token': self.authToken,
            'Content-Type': 'application/json',
            }
            response = requests.request("GET", url, headers=headers, verify=verifySSL)
            templateData = json.loads(response.text)

            #Create template path folder if not exists already
            if not os.path.exists(path):
                os.mkdir(path)

            #Creates one subfolder per template, containting separate files for parameters and content
            templatePath = path+templateData['name']
            if not os.path.exists(templatePath):
                os.mkdir(templatePath)

            #Create a file for the actual content:
            contentsFilename = templatePath +"/"+ templateData['name'] + "_contents.txt"
            with open(contentsFilename, 'w') as out:
                templateParams = templateData['templateContent']
                out.write(str(templateParams))

            #Create a file for all parameters:
            paramsFilename = templatePath +"/"+ templateData['name'] + "_params.json"
            with open(paramsFilename, 'w') as out:
                templateParams = templateData
                if 'templateContent' in templateParams:
                    del templateParams['templateContent']
                out.write(str(json.dumps(templateParams, indent=4)))            

        if path == "":
            path = "local folder"
        if projectName != None:
            return "All templates in project: " + projectName + " are synced to: " + path        
        else:
            return "All templates in all projects are synced to: " + path        




    def pushTemplates(self, **kwargs):
        path = ""
        try:
            path = kwargs['path']
        except:
            pass

        #Createa a reference dict for each templatefolder:
        templatesList = []
        listdir = os.listdir(path)
        folders = []
        for obj in listdir:
            if not re.match(r"^\.", obj):
                folders.append(obj)

        for folder in folders:
            templateDict = {"name" : folder}
            templateName = folder
            templatePath = path+folder

            for file in os.listdir(path+folder):
                if re.match(r'.*_params.json', file):
                    templateDict['paramsFile'] = templatePath  +"/"+file                

                if re.match(r'.*_contents.txt', file):
                    templateDict['contentsFile'] = templatePath +"/"+file

            templatesList.append(templateDict)
        print(templateDict)

        #Firest check if template already exists:
        for template in templatesList:

            #Opening both files
            #Content from the _content.json file:
            templateContents = str(open(template['contentsFile'], 'r').read())
        
            #All parameters from the params file:
            with open(template['paramsFile']) as templateData:
                templateFile = json.load(templateData)
                templateName = templateFile['name']
                projectName = templateFile['projectName']
                
                #Check whats already existing, based on project/template tree name
                url = "https://" + self.ip + ":" + self.port + baseurl + "template-programmer/project/"
                payload = {}
                headers = {
                  'x-auth-token': self.authToken,
                'Content-Type': 'application/json',
                }
                response = requests.request("GET", url, headers=headers, data = payload, verify=verifySSL)
                data = json.loads(response.text)
                templateExists = False
                projectExists = False
                for project in data:
                    if project['name'] == projectName:
                        projectExists = True
                        projectId = project['id']
                        print ("Project exists: " + projectName + " - " + projectId)        

                        for templates in project['templates']:
                            if templates['name'] == templateName:
                                templateId = templates['id']
                                templateExists = True
                                print ("Template exists: " + templateName + " - " + templateId)


                if projectExists == False:
                    print ("Creating missing project: " + projectName)
                    url = "https://" + self.ip + ":" + self.port + "/dna/intent/api/v1/template-programmer/project"

                    payload = {
                          "name": projectName,
                            }
                    headers = {
                      'x-auth-token': self.authToken,
                    'Content-Type': 'application/json',
                    }
                    response = requests.request("POST", url, headers=headers, json=payload, verify=verifySSL)
                    data = json.loads(response.text)
                    
                    #Since the project didn't exist, we need to fetch it's new id. 
                    taskId = data['response']['taskId']
                    datafromtask = self.taskStatus(id=taskId)                    
                    projectId = datafromtask['data']

                if templateExists == False:
                    print ("Creating missing template: "+ templateName)

                    url = "https://" + self.ip + ":" + self.port + "/dna/intent/api/v1/template-programmer/project/" + projectId +"/template"
                    payload = templateFile                
                    #Remove keys, making the payload suitable for new-creation of template. Hence removing id etc.
                    if 'id' in payload:
                        del payload['id']
                    for param in payload['templateParams']:
                        if 'id' in param:
                            del param['id']

                    for param in payload['templateParams']:
                        if 'selection' in param:
                            del param['selection']

                    payload['templateContent'] = str(templateContents)
                    
                    headers = {
                      'x-auth-token': self.authToken,
                    'Content-Type': 'application/json',
                    }
                    response = requests.request("POST", url, headers=headers, json=payload, verify=verifySSL)
                    data = json.loads(response.text)
                    try:
                        self.taskId = data['response']['taskId']
                    except:
                        self.taskId = None

                if templateExists == True:
                #Since the template exists, PUT the file from directory to make sure the active template is same version.
                    print ("Template " + templateName + " already exists, versioning and updating.")

                    headers = {
                      'x-auth-token': self.authToken,
                    'Content-Type': 'application/json',
                    }

                    versionUrl = "https://" + self.ip + ":" + self.port + baseurl + "template-programmer/template/version"
                    versionPayload = {
                    'comments': 'Updated with EZDNAC', 
                    'templateId': templateId
                    }
                    requests.post(versionUrl, headers=headers, json=versionPayload, verify=verifySSL)
                    
                    url = "https://" + self.ip + ":" + self.port + baseurl + "template-programmer/template/"
                    payload = templateFile
                    payload['id'] = templateId

                    for params in payload['templateParams']:
                        del params['id']

                    for param in payload['templateParams']:
                        if 'selection' in param:
                            del param['selection']

                    payload['templateContent'] = templateContents


                    response = requests.request("PUT", url, headers=headers, json=payload, verify=verifySSL)
                    data = json.loads(response.text)
