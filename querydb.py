import pymongo

uri = 'mongodb://frog:Treefort@ds251598.mlab.com:51598/streets'
client = pymongo.MongoClient(uri)
db = client['streets']
streets = db['store_1923']

# sectors = ["\'E2\\", "\'W1\\", "\'NW1\\", "\'NW2\\", "\'SE2\\", "\'SW2\\", "\'NE1\\", "\'W2\\", "\'SW1\\", "\'NW3\\", "\'SE1\\", "\'E1\\"]
#
# for sector in sectors:
#     jsob = {
#         "sector": sector
#     }
#     streets.delete_many(jsob)
#

zips = streets.distinct("zip code")
print( zips )
