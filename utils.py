import requests
import yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

baseUrl = config["paperless-ngx"]["host"]+":"+config["paperless-ngx"]["port"]
token = config["paperless-ngx"]["token"]

def get_correspondents():

    dictionary = {}
    # URL del endpoint
    url = baseUrl+"/api/correspondents/"

    # Headers con el token
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    # Verificar respuesta
    if response.status_code == 200:
        correspondets = response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")

    for i in correspondets["results"]:
        dictionary[i["name"]]=i["id"]
    
    return dictionary


def add_correspondent(name):
    # URL del endpoint
    url = baseUrl+"/api/correspondents/"

    print(url)
    print(token)
    # Headers con el token
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    body = {
        "name": name,
        "match":"",
        "matching_algorithm":6,
        "is_sensitive":True,
        "owner":3,

    }
    response = requests.post(url, headers=headers, json=body)

    # Verificar respuesta
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")


def get_tags():

    dictionary = {}
    # URL del endpoint
    url = baseUrl+"/api/tags/"

    # Headers con el token
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    # Verificar respuesta
    if response.status_code == 200:
        tags = response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")

    for i in tags["results"]:
        dictionary[i["name"]]=i["id"]
    
    return dictionary


def add_tag(name):
    # URL del endpoint
    url = baseUrl+"/api/tags/"

    # Headers con el token
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    body = {
        "name": name,
        "match":"",
        "matching_algorithm":6,
        "is_sensitive":True,
        "owner":3,

    }
    response = requests.post(url, headers=headers, json=body)

    # Verificar respuesta
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")


def get_documentType():

    dictionary = {}
    # URL del endpoint
    url = baseUrl+"/api/document_types/"

    # Headers con el token
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    # Verificar respuesta
    if response.status_code == 200:
        documentType = response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")

    for i in documentType["results"]:
        dictionary[i["name"]]=i["id"]
    
    return dictionary


def add_documenType(name):
    # URL del endpoint
    url = baseUrl+"/api/document_types/"

    # Headers con el token
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    body = {
        "name": name,
        "match":"",
        "matching_algorithm":6,
        "is_sensitive":True,
        "owner":3,

    }
    response = requests.post(url, headers=headers, json=body)

    # Verificar respuesta
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")




def upload_document(document, title, created=None, correspondent=None, document_type=None, tags=None, file="image/jpg"):

    # URL del endpoint
    url = baseUrl+"/api/documents/post_document/"

    # Token de autenticación

    # Headers con el token
    headers = {
        "Authorization": f"Token {token}",
    }
    body = {
        #"document": document,
        "name":title,
        "storage_path":1,
        "owner":3,
    }

    files = {
    "document": (title+".jpg", document, "image/jpeg")
    }

    


    if created != "":
        body["created"] = created

    if correspondent != "":
        body["correspondent"] = correspondent

    if document_type != "":
        body["document_type"] = document_type


    if len(tags)>0:
        body["tags"] = [int(i) for i in tags]
    
    print(str(body))
    response = requests.post(url, headers=headers, files=files, data=body)

    if response.ok:
        print(response.json())
    else:
        print(response.status_code, response.text)

