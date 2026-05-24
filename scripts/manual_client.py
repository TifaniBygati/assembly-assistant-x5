import requests
import json

base_url = "http://127.0.0.1:8000"

payload = {
  "order_id": "0327",
  "street": "Урицкого",
  "house": "28",
  "apartment": "65",
  "phone": "+88005553535",
  "comment": "+88005553536"
}

patch = {'phone': '+88005553535'}

def check_health(base_url):

    response = requests.get(f"{base_url}/health",timeout=5)

    return response

def get_all_clients(base_url):

    response = requests.get(f"{base_url}/clients",timeout=5)

    result = json.dumps(response.json(), ensure_ascii=False, indent=4)

    return result

def post_client(base_url, payload):
    response = requests.post(f"{base_url}/clients",json=payload,timeout=5)
    return response


def get_search_client(base_url):
    response = requests.get(f"{base_url}/clients/search",params={'street':'Пушкина','house':'7'},timeout=5)
    result = json.dumps(response.json(), ensure_ascii=False, indent=4)
    return result

def search_client_by_id(base_url,client_id):
    response = requests.get(f"{base_url}/clients/{client_id}",timeout=5)

    result = json.dumps(response.json(), ensure_ascii=False, indent=4)
    return result

def patch_client(base_url,client_id, patch):
    response = requests.patch(f"{base_url}/clients/{client_id}",json=patch,timeout=5)

    result = json.dumps(response.json(), ensure_ascii=False, indent=4)
    return result

def delete_client(base_url,client_id):

    response = requests.delete(f"{base_url}/clients/{client_id}",timeout=5)
    return json.dumps(response.json(), ensure_ascii=False, indent=4)

#print(check_health(base_url).status_code)
#print(check_health(base_url).json())

#print(get_all_clients(base_url))

print(post_client(base_url, payload).text)#так и не понял в чём ошибка payload вроде всё правельно но ловлю 422msg":"Input should be a valid dictionary or object to extract fields from","input":"order_id=0327&street=%D0%A3%D1%80%D0%B8%D1%86%D0%BA%D0%BE%D0%B3%D0%BE&house=28&apartment=65&phone=%2B88005553535&comment=%2B88005553536"

#print(get_search_client(base_url))

#print(search_client_by_id(base_url,1))

print(patch_client(base_url,1,patch))

#print(delete_client(base_url,1))






