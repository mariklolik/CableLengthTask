import json
import requests


def get_coord(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('ERROR')
        exit(0)

    json_response = response.json()
    with open('response.json', 'w', encoding='utf-8') as file:
        json.dump(json_response, file, indent=2, ensure_ascii=False)
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    city = toponym['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea'][
        'SubAdministrativeArea']['Locality']['LocalityName']

    long, latt = toponym["Point"]['pos'].split(' ')
    return long, latt


def get_elevation(long, latt):
    elevation_api_server = f'https://api.opentopodata.org/v1/aster30m?locations={latt},{long}'
    # Dataset aster30m
    response = requests.get(elevation_api_server)
    json_response = response.json()
    with open('elelvation_response.json', 'w', encoding='utf-8') as file:
        json.dump(json_response, file, indent=2, ensure_ascii=False)

    return json_response["results"][0]["elevation"]


def get_height(lon, lat):
    elev = get_elevation(lon, lat)
    return elev


def get_city_coord(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('ERROR')
        exit(0)

    json_response = response.json()
    with open('response.json', 'w', encoding='utf-8') as file:
        json.dump(json_response, file, indent=2, ensure_ascii=False)
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    city = toponym['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea'][
        'SubAdministrativeArea']['Locality']['LocalityName']

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": city,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('ERROR')
        exit(0)

    json_response = response.json()
    with open('response_city.json', 'w', encoding='utf-8') as file:
        json.dump(json_response, file, indent=2, ensure_ascii=False)
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    long, latt = toponym["Point"]['pos'].split(' ')
    return long, latt


def manhattan_dist(x1, y1, x2, y2):
    x1, y1, x2, y2 = [float(i) for i in [x1, y1, x2, y2]]
    return abs(x1 - x2) + abs(y1 - y2)


def calculate_inside(lon, lat, lon_c, lat_c):
    return abs(get_height(lon, lat) - get_height(lon_c, lat_c)) * 2


def main():
    length = 0
    toponym_to_find = ''
    lon, lat = 0, 0
    while True:

        toponym_to_find = input()
        if toponym_to_find == 'exit':
            break
        lon_new, lat_new = get_coord(toponym_to_find)
        if (lon, lat) != (0, 0):
            length += manhattan_dist(lon, lat, lon_new, lat_new) * 100 * 1000

        lon, lat = lon_new, lat_new

        lon_c, lat_c = get_city_coord(toponym_to_find)
        length += calculate_inside(lon, lat, lon_c, lat_c)
        print(f"LENGTH:{int(length)} meters")


if __name__ == "__main__":
    main()
