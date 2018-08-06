import pymongo
import csv
import pandas as pd
import sys

def main(store_num):
    dfs = groupCitiesByStreet(store_num)
    fdf = createSectorsFromStreets(store_num, dfs)
    saveSectorData(store_num, fdf)

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

def consolidateStreets(lists):
    i = 1
    while i < len(lists):
        if (lists[i][0] == lists[i-1][0]):
            lists[i-1][1] = lists[i-1][1] + ", " + lists[i][1]
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
                lists[i][3] = int(lists[i][3]) + 99 - end_remainder
            i += 1
    return lists

def convertSectorDataFrame(frame):
    data = dataFrameToListOfTuples(frame)
    data = sorted(set(data), key=lambda a: (a[0], a[1], a[2], a[3]))
    data = listOfLists(data)
    data = consolidateSectors(data)
    data = resetMinMax(data)
    return data

def groupCitiesByStreet(store_num):
    street_filename = 'Streets_' + store_num[-4:] + '.csv'
    df = pd.read_csv(street_filename)
    if 'down' in df:
        df = df.drop(['down'], axis=1)
    rows = buildStreetsCitiesList(df)
    rdf = pd.DataFrame(rows, columns = ['street name', 'cities'])
    rdf = rdf.groupby(by='street name')
    return rdf

def buildStreetsCitiesList(df):
    rows = []
    for row in df.iterrows():
        if ('(' in str(row[1].values)):
            streetname, city = row[1].values[0].split(" (")
            city = city.replace(')', '')
            rows.append([streetname, city])
    return rows

def createSectorsFromStreets(store_num, df):
    dft = dbConnectToDataFrame(store_num)
    sector_data = convertSectorDataFrame(dft[['sector', 'street name', 'street numbers.starting', 'street numbers.ending']])
    sectordf = pd.DataFrame(sector_data, columns = ['sector', 'street name', 'starting', 'ending'])
    rows = buildSectorList(df, sectordf)
    rdf = pd.DataFrame(rows, columns = ['sector', 'street name', 'starting', 'ending'])
    rdf = rdf.sort_values(['sector', 'street name', 'starting', 'ending'], ascending=[True, True, True, True])
    rdf['parity'] = 0
    return rdf

def buildSectorList(df, sectordf):
    rows = []
    for row in df:
        cvs = row[1]['cities'].values
        dfrow = sectordf[sectordf['street name']==row[0]].values
        for city in cvs:
            for sector in dfrow:
                temp = sector.copy()
                if (sector[2]==sector[3]):
                    temp[1] = sector[1] + ' (' + city  + ') $'
                else:
                    temp[1] = sector[1] + ' (' + city  + ')'
                rows.append(temp)
    return rows

def saveSectorData(store_num, df):
    sector_filename = 'Sectors_' + store_num[-4:] + '.csv'
    df.to_csv(sector_filename, index=False)
    print(sector_filename + ' saved successfully!')

if __name__ == "__main__":
    store_num = 'store_'+str(sys.argv[1])
    main(store_num)
