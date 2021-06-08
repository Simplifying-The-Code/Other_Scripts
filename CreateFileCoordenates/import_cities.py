# The simple is just the beginning to open your mind of how everything works in a simple way. "GuiDeLuccaDev"

''' A python script to create a file with coordinates 
    for use in locating or collecting data from some api. '''

import csv
import json
from unicodedata import normalize
 
def no_accentuation(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

cities_name = open("cities.csv", "r", encoding="utf8").readlines()
cities_coord = open("coordenates.csv", "r", encoding="utf8").readlines()

cities_coordenates = {}

for city in cities_name:
    city_code, city_uf, city_name = city.split(";")
    for coord in cities_coord:
        coord_code, coord_lat, coord_lon = coord.split(";")
        if city_code in coord_code:
            cities_coordenates[no_accentuation(city_name)] = {"uf": city_uf, "lat": coord_lat, "lon": coord_lon}
            break
        continue
    continue
    
with open("result.json", "w") as json_file:
    json.dump(cities_coordenates, json_file, indent=4)



