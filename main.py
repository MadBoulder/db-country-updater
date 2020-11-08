from geopy.geocoders import Nominatim
import os
import json
import time

def monkey_patch_geopy_base(instance, lang='en'):
    instance.headers['Accept-Language'] = lang


def main(db_path='../BetaLibrary/', is_update=True):
    # walk all data
    areas = next(os.walk(db_path + 'data/zones/'))[1]
    for area in areas:
        time.sleep(1) # rate limiter (as per Geopy's documentation)
        # Load zone data
        datafile = db_path + 'data/zones/' + area + '/' + area + '.txt'
        with open(datafile, encoding='utf-8') as data:
            area_data = json.load(data)
        if is_update and area_data.get('country', ''):
            print(f'Skipping update for {area_data["name"]}')
            continue
        lat = area_data['latitude']
        lng = area_data['longitude']
        # The geopy installation has been modified to return countries in English
        geolocator = Nominatim(user_agent='my_email@myserver.com')
        monkey_patch_geopy_base(geolocator, lang='en')
        location = geolocator.reverse(f"{lat}, {lng}")
        country_code = location.raw['address']['country_code']
        # print(location.raw)
        print(area_data['name'], country_code)
        # print(location.address)

        area_data['country'] = country_code
        with open(datafile, 'w', encoding='utf-8') as data:
           json.dump(area_data, data, indent=4)

if __name__ == "__main__":
    main(is_update=False)
