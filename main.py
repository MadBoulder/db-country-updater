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
        time.sleep(1)
        # Load data zone map
        datafile = db_path + 'data/zones/' + area + '/' + area + '.txt'
        area_data = {}
        with open(datafile, encoding='utf-8') as data:
            area_data = json.load(data)
        if is_update and area_data.get('country', ''):
            print(f'Skipping update for {area_data["name"]}')
            continue
        lat = area_data['latitude']
        lng = area_data['longitude']
        # The geopy installation has been modified to return countries un English
        geolocator = Nominatim(user_agent='my_email@myserver.com')
        monkey_patch_geopy_base(geolocator, lang='es')
        location = geolocator.reverse(f"{lat}, {lng}")
        found_country = location.raw['address']['country']
        # print(location.raw)
        print(area_data['name'], found_country)
        print(location.address)

        area_data['country'] = found_country
        with open(datafile, 'w', encoding='utf-8') as data:
           json.dump(area_data, data, indent=4)

if __name__ == "__main__":
    main(is_update=False)