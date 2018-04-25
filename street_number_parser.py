from shapely.geometry import Polygon
from shapely.geometry import Point
import os
import time
import keys
import sectorPolygons7371
import requests
import threading
import json
import csv
import pandas as pd
import operator
from random import shuffle
import pdb
import pymongo
import queue
from time import sleep
import sys
from RedisQueue import RedisQueue



class request_getter(threading.Thread):
    def __init__(self, q, store_num):
        threading.Thread.__init__(self)
        self.q = q
        self.store_num = store_num
        self.uri = 'mongodb://frog:Treefort@ds251598.mlab.com:51598/streets'
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client['streets']
        self.streets = self.db[self.store_num]
        self.keyNum = 0
        self.requests = 0


    def run(self):
        while (self.keyNum < len(keys.keys)):

            self.setKey(self.keyNum)

            # Recent change
            coords = str(self.q.get())[3:-2].split(', ')
            self.addresses = []
            self.sectorName, self.x, self.y = coords
            self.sectorName = self.sectorName.replace('"', '').replace("'", '').replace('\\', '')
            self.x = self.x.replace('"', '').replace("'", '').replace('\\', '')[0:9]
            self.y = self.y.replace('"', '').replace("'", '').replace('\\', '')[0:10]
            print('[', self.sectorName, self.x, self.y, ']')
            if (self.streets.find({"coordinates": {
                "latitude": self.x,
                "longitude": self.y
            }}).count() > 0):
                print("Already exists in database.")
                continue
            self.make_request(self.x, self.y)

    def setKey(self, index):
        self.key = keys.keys[index][1]

    def make_request(self, lat, lon):
        # Recent change
        URL_STRING = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}".format(lat, lon, self.key)
        r = requests.get(URL_STRING)

        self.requests += 1
        ret = r.json()
        try:
            city = ''
            zipcode = ''

            numbers = ret['results'][0]['address_components'][0]['short_name']
            streetName = ret['results'][0]['address_components'][1]['short_name']
            try:
                city = ret['results'][0]['address_components'][2]['short_name']
            except:
                pass
            try:
                zipcode = ret['results'][0]['address_components'][6]['short_name']
                if (not zipcode.isdigit()):
                    zipcode = ret['results'][0]['address_components'][7]['short_name']
            except:
                pass

            startEnd = numbers.split('-')
            if (len(startEnd) == 1):
                startEnd.append(startEnd[0])

            if (startEnd[0].isdigit() and startEnd[1].isdigit()):
                if (int(startEnd[0]) > int(startEnd[1])):
                    temp = startEnd[0]
                    startEnd[0] = startEnd[1]
                    startEnd[1] = temp

                if (int(startEnd[0]) <= int(startEnd[1])):
                    if ("MN-3" in streetName):
                        streetName = "S Robert Trail"

                    if ("County" in streetName):
                        if ("Rd 56" in streetName):
                            streetName = "Concord Blvd E"
                        elif ("Rd 73" in streetName):
                            streetName = "Babcock Trail"
                        elif ("Rd 18" in streetName):
                            streetName = "Upper 55th St E"

                    #print(str(self.requests) + " " + self.sectorName + " " + str(lat) + "," + str(lon) + " start:" + str(startEnd[0]) + " end:" + str(startEnd[1]) + " " + streetName + ", " + city + " " + zipcode)
                    self.addresses.append((self.sectorName, str(lat), str(lon), str(startEnd[0]), str(startEnd[1]), streetName, city, zipcode))
                    jsob = {
                            "sector": self.sectorName,
                            "coordinates": {
                                "latitude": lat,
                                "longitude": lon
                            },
                            "street numbers": {
                                "starting": startEnd[0],
                                "ending": startEnd[1]
                            },
                            "street name": streetName,
                            "city": city,
                            "zip code":zipcode
                    }

                    filt = {
                        "sector": self.sectorName,
                        "coordinates": {
                            "latitude": lat,
                            "longitude": lon
                        }
                    }

                    result = self.streets.replace_one(filt, jsob, True)

        except IndexError:
            if (self.keyNum <= len(keys.keys)):
                self.q.put((self.sectorName, self.x, self.y))
                print('Switching keys to key number ' + str(self.keyNum + 2))
                self.keyNum += 1
                try:
                    self.setKey(self.keyNum)
                    self.make_request(lat,lon)

                except IndexError:
                    print("You've reached the maximum number of requests for today")
                    self.keyNum = len(keys.keys)*2


class generateSectors(threading.Thread):
    def __init__(self, sector, keynum, q, store_num):
        threading.Thread.__init__(self)
        self.keyNum = keynum
        self.key = ''
        self.sectorName = ''
        self.bounds = []
        self.sw = Point(0,0)
        self.ne = Point(0,0)
        self.point_inc = Point(0,0)
        self.polygon = sector
        self.requests = 0
        self.addresses = []
        self.uri = 'mongodb://frog:Treefort@ds251598.mlab.com:51598/streets'
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client['streets']
        self.store_num = store_num
        self.streets = self.db[self.store_num]
        self.q = q
        self.areaNum = 0

    def run(self):
        self.set_starting_conditions(self.polygon[0], self.polygon[1])
        print(self.sectorName)
        print(self.shape)
        self.point_inc = Point(self.sw.x-.002, self.ne.y-.002)
        self.cords = []
        while(self.point_inc.x < self.ne.x):
            while(self.point_inc.y < self.ne.y):
                self.cords.append((self.point_inc.x, self.point_inc.y))
                self.inc_y()
            self.inc_x()

        shuffle(self.cords)

        for i in self.cords:
            self.point_inc = Point(i[0], i[1])
            if (self.point_inc.within(self.shape)):
                # if (self.streets.find({"coordinates": {
                #     "latitude": self.point_inc.x,
                #     "longitude": self.point_inc.y
                # }}).count() > 0):
                #     print("Already exists in database.")
                #     continue
                # else:
                self.q.put((self.sectorName, self.point_inc.x, self.point_inc.y))
            else:
                continue

        print('End of sector')

    def setKey(self, index):
        if index<len(keys.keys):
            self.key = keys.keys[index][1]

    def set_sector_name(self, name):
        self.sectorName = name

    def set_bounds(self, border):
        self.bounds = border

    def make_shape(self):
        self.shape = Polygon(self.bounds)

    def set_starting(self):
        self.point_inc = Point(self.sw.x, self.sw.y)

    def set_corners(self):
        self.sw = Point((min(self.bounds, key=lambda point:point[0])[0]-.001),(min(self.bounds, key=lambda point:point[1])[1]-.001))
        self.ne = Point((max(self.bounds, key=lambda point:point[0])[0]+.0015),(max(self.bounds, key=lambda point:point[1])[1]+.0015))

    def inc_x(self):
        self.point_inc = Point(self.point_inc.x + 0.00025, self.sw.y)

    def inc_y(self):
        self.point_inc = Point(self.point_inc.x, self.point_inc.y + 0.00025)

    def set_starting_conditions(self, name, vertices):
        self.set_sector_name(name)
        self.set_bounds(vertices)
        self.set_corners()
        self.set_starting()
        self.make_shape()

def main(run_type, store_num):
    q = RedisQueue(store_num)
    if run_type == 'gen':
        for i in range(len(sectorPolygons7371.sectors)):
            s = generateSectors(sectorPolygons7371.sectors[i], i, q, store_num)
            print('starting this thread')
            s.start()

    elif run_type == 'run':
        uri = 'mongodb://frog:Treefort@ds251598.mlab.com:51598/streets'
        client = pymongo.MongoClient(uri)
        db = client['streets']
        streets = db[store_num]
        streets.create_index([("latitude", pymongo.DESCENDING), ("longitude",  pymongo.DESCENDING)])
        for i in range(30):
            rg = request_getter(q, store_num)
            print('starting request thread')
            rg.start()

        while q.qsize():
            sleep(10)
            print(q.qsize())

if __name__ == "__main__":
    run_type = sys.argv[1]
    store_num = 'store_'+str(sys.argv[2])
    main(run_type, store_num)
