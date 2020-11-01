import requests
import os
import sys

server = 'XXXXXXXX'

# Setup initial connection to the server
url = (server + '/icws/connection')
body = {"__type":"urn:inin.com:connection:icAuthConnectionRequestSettings",
        "applicationName":"Create Email and add an attachment",
        "userID": "username",
        "password": "password"} 
connection = requests.post(url, json = body, headers = {"Accept-Language": "en-us"})
if connection.status_code >= 200 and  connection.status_code <= 299:
    jsonresult=connection.json()
    token = jsonresult['csrfToken']
    sessionID = jsonresult['sessionId']
    cookie = connection.cookies.get_dict()
else:
    print(connection.text)
    exit()

# creates a new email interaction
url = (server + "/icws/" + sessionID + "/interactions")
body = {"emailContent":
            {"sender":
                   {"displayName":"XXXXXXX","address":"example@example.com"},
            "bodies":[{"body":"​Example e-mail body","bodyType":0},{"body":"<html><body><div>​Example e-mail body</div></body></html>",
            "bodyType":1}],
            "__type":"urn:inin.com:interactions.email:emailContent"},
            "workgroup":"CallWorkgroup",
            "__type":"urn:inin.com:interactions.email:createEmailParameters"}
connection = requests.post(url, json = body, headers = {"ININ-ICWS-CSRF-Token" : token}, cookies = cookie)
jsonresult=connection.json()
interactionID = jsonresult['interactionId']
if connection.status_code >= 200 and  connection.status_code <= 299:
    print("Created new interaction {}".format(interactionID))
else:
    print(connection.text)
    exit()
    
#gets the URI for to HTTP upload the file
url = (server + "/icws/" + sessionID + "/interactions/" + interactionID +"/email/attachments/file/upload")
body = {"isInlineAttachment":"true",
       "uploadFileName":"test.txt"
       }
connection = requests.post(url, json = body, headers = {"ININ-ICWS-CSRF-Token" : token}, cookies = cookie)
if connection.status_code >= 200 and  connection.status_code <= 299:
    jsonresult=connection.json()
    uploaduri = jsonresult['uploadUri']
else:
    print(connection.text)
    exit()

#Doing the actual HTTP upload
url =(server + uploaduri)
filename = ("test.txt")
files = {'file': open(filename)}
connection = requests.post(url, headers = {"ININ-ICWS-CSRF-Token" : token}, cookies = cookie, files = files)
if connection.status_code >= 200 and connection.status_code <= 299:
   print("Attachment uploaded")
else:
   print(connection.text)

#Delete the session on CIC
url = (server + "/icws/" + sessionID + "/connection")
connection = requests.delete(url, headers = {"ININ-ICWS-CSRF-Token" : token}, cookies = cookie)
if connection.status_code >= 200 and connection.status_code <= 299:
   print("session closed")
else:
   print(connection.text)
