import glob
import os
import csv
import pandas as pd
import sys
import re

def execute(store_num):
    dfs = setStreetMinMax(store_num)
    saveRangeData(store_num, dfs)

def setStreetMinMax(store_num):
    sector_filename = 'Sectors_' + store_num + '.csv'
    df = pd.read_csv(sector_filename)
    df = df.drop(['sector', 'parity'], axis=1)
    rows = removeCity(df.values.tolist())
    rows = sorted(rows, key=lambda a: (a[0], a[1], a[2]))
    rows = consolidateRanges(rows)
    rdf = pd.DataFrame(rows, columns = ['Street Name', 'Lowest', 'Highest'])
    rdf = rdf.sort_values(by=['Street Name'])
    return rdf

def removeCity(lists):
    for i in range(len(lists)):
        lists[i][0] = re.sub(r" \(.+$", "", lists[i][0])
    return lists

def consolidateRanges(lists):
    i = 1
    while i < len(lists):
        if (lists[i][0] == lists[i-1][0]):
            lists[i-1][1] = min(int(lists[i-1][1]), int(lists[i][1]), int(lists[i-1][2]), int(lists[i][2]))
            lists[i-1][2] = max(int(lists[i-1][1]), int(lists[i][1]), int(lists[i-1][2]), int(lists[i][2]))
            lists.pop(i)
        else:
            i += 1
    return lists

def saveRangeData(store_num, df):
    ranges_filename = 'Ranges_' + store_num + '.csv'
    df.to_csv(ranges_filename, index=False)
    print(ranges_filename + ' saved successfully!')

for folder in glob.glob('./' + ('[0-9]' * 4)):
    os.chdir(folder)
    execute(folder.replace('.\\', ''))
    os.chdir('..')
