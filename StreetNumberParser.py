import requests
import json
import pandas as pd

STARTING_LAT= 44.890774
LAT_INC  = STARTING_LAT
STARTING_LONG = -93.000847
LONG_INC = STARTING_LONG
ENDING_LAT = 44.993612
ENDING_LONG = -92.862771

addresses = []

while(LAT_INC <= ENDING_LAT):

    while(LONG_INC <= ENDING_LONG):
        URL_STRING = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(LAT_INC) + "," + str(LONG_INC) + "&key=AIzaSyCz5ryOD2HZ5B4WhTadfM7Yza54NuMfTBw"
        r = requests.get(URL_STRING)
        print(URL_STRING)
        if (not isempty(r.json())):
            ret = r.json()
            numbers = ret['results'][0]['address_components'][0]['short_name']
            streetName = ret['results'][0]['address_components'][1]['short_name']
            addresses.append((str(LAT_INC) + "," + str(LONG_INC), numbers, streetName))
            print(results)
        LONG_INC += 0.0004

    LAT_INC += .0004
    LONG_INC = STARTING_LONG

df = pd.DataFrame(addresses)
df.columns = ['GPS Coordinates', 'Address']
df.to_csv('addresses.csv', index=False)
