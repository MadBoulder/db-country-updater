# db-country-updater
Update MadBoulder's database by adding countries to zones. 

By using [Geopy](https://github.com/geopy/geopy) it is possible to perform reverse geolocation and, given a pair of coordinates, get the address of the location. Once the address is known, it is trivial to get the country. 

A part from that, this piece of code adds a new field in each zone's JSON file where the country is specified, in english.

**Note**:
Once this is working it should be moved to BetaLibrary's main repo and be part of the page/template generation.