import pygame
import requests
import os


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
address_ll = "37.588392,55.734036"
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
    print(search_params)
    print("Http статус:", response.status_code, "(", response.reason, ")")

json_response = response.json()
organizations = json_response["features"][:10]
met = ''
for i in organizations:
    cords = ','.join([str(p) for p in i['geometry']['coordinates']])
    tp = i['properties']['CompanyMetaData']['Hours'].get('text', 'not found')
    if tp == 'not found':
        met += f'~{cords},pm2grm'
    elif 'круглосуточно' in tp:
        met += f'~{cords},pm2gnm'
    else:
        met += f'~{cords},pm2dbm'

params = {
    "l": "map",
    "pt": met[1:]
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(params)
    print("Http статус:", response.status_code, "(", response.reason, ")")

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)



