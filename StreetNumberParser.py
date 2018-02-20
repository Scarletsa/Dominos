import requests
import json
import pandas as pd

#AIzaSyBFMeWnJ83i8-Bb-UUtJD0HgYhWC7Narys  1901 API key
#AIzaSyCz5ryOD2HZ5B4WhTadfM7Yza54NuMfTBw  personal API key
key1901 = 'AIzaSyBb1yDgS5mrnimYWcwnLWApbtgRZFZ1h74'
keyFuyu = 'AIzaSyCz5ryOD2HZ5B4WhTadfM7Yza54NuMfTBw'
keyBushido = 'AIzaSyB_PSBGppq3vGjYj01OUNwT7XCtE5-S7Ns'

STARTING_LAT= 44.936838
LAT_INC  = STARTING_LAT
STARTING_LONG = -92.959038
LONG_INC = STARTING_LONG
ENDING_LAT = 44.963421
ENDING_LONG = -92.934031
increment = 0

addresses = []

while(LAT_INC <= ENDING_LAT):

    while(LONG_INC <= ENDING_LONG):
        increment += 1
        URL_STRING = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" \
         + str(LAT_INC) + "," + str(LONG_INC) + "&key=" + key1901
        r = requests.get(URL_STRING)
        print(increment)
        ret = r.json()
        numbers = ret['results'][0]['address_components'][0]['short_name']
        streetName = ret['results'][0]['address_components'][1]['short_name']
        addresses.append((str(LAT_INC), str(LONG_INC), numbers, streetName))
        print(str(LAT_INC) + "," + str(LONG_INC) + " " + numbers + " " + streetName)
        LONG_INC += 0.0005

    LAT_INC += .0005
    LONG_INC = STARTING_LONG

df = pd.DataFrame(addresses)
df.columns = ['Lat','Long', 'Numbers', 'Name']
df.to_csv('Woodbury-A1-addresses.csv', index=False)
