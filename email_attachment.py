import requests
import os
import sys

server = 'XXXXXXXX'

def connection(server):
    url = (server + '/icws/connection')
    body = {"__type":"urn:inin.com:connection:icAuthConnectionRequestSettings",
    "applicationName":"Create Email and add an attachment",
    "userID": "username",
    "password": "password"} 
    connection = requests.post(url, json = body, headers = {"Accept-Language": "en-us"})
    if connection.status_code >= 200 and  connection.status_code <= 299:
        jsonresult=connection.json()
        global token
        token = jsonresult['csrfToken']
        global sessionID
        sessionID = jsonresult['sessionId']
        global cookie
        cookie = connection.cookies.get_dict()
    else:
        print(connection.text)
        exit()
connection(server)

def createEmail(server):
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
    global interactionID
    interactionID = jsonresult['interactionId']
    if connection.status_code >= 200 and  connection.status_code <= 299:
        print("Created new interaction {}".format(interactionID))
    else:
        print(connection.text)
        exit()
createEmail(server)    

def getuploadUri(server):
    url = (server + "/icws/" + sessionID + "/interactions/" + interactionID +"/email/attachments/file/upload")
    body = {
    "isInlineAttachment":"true",
    "uploadFileName":"test.txt"
    }
    connection = requests.post(url, json = body, headers = {"ININ-ICWS-CSRF-Token" : token}, cookies = cookie)
    if connection.status_code >= 200 and  connection.status_code <= 299:
        jsonresult=connection.json()
        global uploaduri
        uploaduri = jsonresult['uploadUri']
    else:
        print(connection.text)
        exit()
getuploadUri(server)
    
def fileupload(server):
    url =(server + uploaduri)
    filename = ("test.txt")
    files = {'file': open(filename)}
    connection = requests.post(url, headers = {"ININ-ICWS-CSRF-Token" : token}, cookies = cookie, files = files)
    if connection.status_code >= 200 and connection.status_code <= 299:
        print("Attachment uploaded")
    else:
        print(connection.text)
fileupload(server)

def close(server):
    url = (server + "/icws/" + sessionID + "/connection")
    connection = requests.delete(url, headers = {"ININ-ICWS-CSRF-Token" : token}, cookies = cookie)
    if connection.status_code >= 200 and connection.status_code <= 299:
        print("session closed")
    else:
        print(connection.text)
close(server)