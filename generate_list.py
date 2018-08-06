import pymongo
import csv
import pandas as pd
import sys

def main(store_num, list_type):
    df = dbConnectToDataFrame(store_num)
    if list_type == 'street':
        street_filename = 'Streets_' + store_num[-4:] + '.csv'
        df['street name'] = df['street name'] + " (" + df['city'] + ")"
        street_data = convertStreetDataFrame(df[['street name']])
        saveStreetData(street_data, street_filename)
    if list_type == 'sector':
        sector_filename = 'Sectors_' + store_num[-4:] + '.csv'
        sector_data = convertSectorDataFrame(df[['sector', 'street name', 'street numbers.starting', 'street numbers.ending']])
        saveSectorData(sector_data, sector_filename)

def dbConnectToDataFrame(store_num):
        uri = 'localhost:27017'
        client = pymongo.MongoClient(uri)
        db = client['streets']
        streets = db[store_num].find()
        norm_data = pd.io.json.json_normalize(list(streets))
        frame = pd.DataFrame(norm_data)
        return frame

def dataFrameToListOfTuples(frame):
    dump = []
    for i in frame.iterrows():
        dump.append(tuple(i[1]))
    return dump

def listOfLists(tups):
    for j in range(len(tups)):
        tups[j] = list(tups[j])
    return tups

def consolidateSectors(lists):
        i = 1
        while i < len(lists):
            if (lists[i][0] == lists[i-1][0] and lists[i][1] == lists[i-1][1]):
                lists[i-1][2] = min(int(lists[i-1][2]), int(lists[i][2]), int(lists[i-1][3]), int(lists[i][3]))
                lists[i-1][3] = max(int(lists[i-1][2]), int(lists[i][2]), int(lists[i-1][3]), int(lists[i][3]))
                lists.pop(i)
            else:
                i += 1
        return lists

def resetMinMax(lists):
    i = 0
    while i < len(lists):
        if (int(lists[i][2]) == int(lists[i][3])):
            i += 1
            pass
        else:
            start_remainder = int(lists[i][2]) % 100
            end_remainder = int(lists[i][3]) % 100
            if (start_remainder < 24):
                lists[i][2] = int(lists[i][2]) - start_remainder
            if (end_remainder > 76):
                lists[i][3] = int(lists[i][3]) + 100 - end_remainder
            i += 1

    return lists

def consolidateStreets(lists):
    i = 1
    while i < len(lists):
        if (lists[i][0] == lists[i-1][0]):
            lists[i-1][1] = lists[i-1][1] + ", " + lists[i][1]
            lists.pop(i)
        else:
            i += 1

    return lists

def convertSectorDataFrame(frame):
    data = dataFrameToListOfTuples(frame)
    data = sorted(set(data), key=lambda a: (a[0], a[1], a[2], a[3]))
    data = listOfLists(data)
    data = consolidateSectors(data)
    data = resetMinMax(data)
    return data

def convertStreetDataFrame(frame):
    data = dataFrameToListOfTuples(frame)
    data = sorted(set(data), key=lambda a: (a[0]))
    data = listOfLists(data)
    return data

def saveSectorData(lists, filename):
    sector_df = pd.DataFrame(lists)
    sector_df.columns = ["sector", "street name", "starting", "ending"]
    sector_df.to_csv(filename, index=False)
    print(filename + ' saved successfully!')

def saveStreetData(lists, filename):
    street_df = pd.DataFrame(lists)
    street_df.columns = ["street name"]
    street_df.to_csv(filename, index=False)
    print(filename + ' saved successfully!')

if __name__ == "__main__":
    store_num = 'store_'+str(sys.argv[1])
    main(store_num, sys.argv[2])
