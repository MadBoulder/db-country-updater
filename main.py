from geopy.geocoders import Nominatim
import os
import json
import time

COUNTRY_KEY = 'country'
COUNTRY_CODE_KEY = 'country_code'
ADDRESS_KEY = 'address'
NAME_KEY = 'name'

def monkey_patch_geopy_base(instance, lang='en'):
    instance.headers['Accept-Language'] = lang


def main(db_path='../BetaLibrary/', is_update=True):
    # walk all data
    areas = next(os.walk(db_path + 'data/zones/'))[1]
    country_dict = {}
    for area in areas:
        time.sleep(1) # rate limiter (as per Geopy's documentation)
        # Load zone data
        datafile = db_path + 'data/zones/' + area + '/' + area + '.json'
        with open(datafile, encoding='utf-8') as data:
            area_data = json.load(data)
        if is_update and area_data.get(COUNTRY_KEY, ''):
            print(f'Skipping update for {area_data[NAME_KEY]}')
            continue
        geolocator = Nominatim(user_agent='my_email@myserver.com')
        # Patch geopy to return countries in English
        monkey_patch_geopy_base(geolocator, lang='en')
        location = geolocator.reverse(f"{area_data['latitude']}, {area_data['longitude']}")
        country = location.raw[ADDRESS_KEY][COUNTRY_CODE_KEY]
        # print(location.raw)
        print(area_data[NAME_KEY], country)
        # print(location.address)

        area_data[COUNTRY_KEY] = country
        with open(datafile, 'w', encoding='utf-8') as data:
           json.dump(area_data, data, indent=4)

def update_single_zone(area, db_path='../BetaLibrary/'):
    datafile = db_path + 'data/zones/' + area + '/' + area + '.json'
    with open(datafile, encoding='utf-8') as data:
        area_data = json.load(data)
    geolocator = Nominatim(user_agent='my_email@myserver.com')
    # Patch geopy to return countries in English
    monkey_patch_geopy_base(geolocator, lang='en')
    location = geolocator.reverse(f"{area_data['latitude']}, {area_data['longitude']}")
    print(location)
    country = location.raw[ADDRESS_KEY][COUNTRY_CODE_KEY]
    # print(location.raw)
    print(area_data[NAME_KEY], country)
    # print(location.address)

    area_data[COUNTRY_KEY] = country
    with open(datafile, 'w', encoding='utf-8') as data:
        json.dump(area_data, data, indent=4)


if __name__ == "__main__":
    # main(is_update=True)
    update_single_zone('ubatuba')
