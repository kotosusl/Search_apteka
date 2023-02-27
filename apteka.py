import sys
import requests
from PIL import Image
from io import BytesIO
import math


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = '37.588392,55.734036'  # ','.join([input('Введите широту: '), input('Введите долготу: ')][::-1])

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(" + response.reason + ")")
    sys.exit(0)

json_response = response.json()

organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
org_time = organization["properties"]["CompanyMetaData"]["Hours"]["Availabilities"][0]["Intervals"][0]
org_hours = f'с {org_time["from"]} до {org_time["to"]}'

point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])

map_params = {
    "l": "map",
    "pt": "{0},pm2bl~{1},pm2al".format(org_point, address_ll)
}
data = {
    "address": org_address,
    "name": org_name,
    "hours": org_hours,
    "distance": math.sqrt((point[0] - float(address_ll.split(',')[0])) ** 2 + (point[1] - float(address_ll.split(',')[1])) ** 2) * 111000
}
print(data)
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()