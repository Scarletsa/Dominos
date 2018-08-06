import pymongo
import sys

def main(store_num):
    uri = 'localhost:27017'
    client = pymongo.MongoClient(uri)
    db = client['streets']
    streets = db[store_num]

    zips = streets.update_many(
        {'city': "Windom Park"},
        { '$set' :{'city':"Minneapolis"}}
    )

    zips = streets.aggregate([
        {
            '$group': {
                '_id': {'city': '$city'},
                'count': { '$sum': 1 }
            }
        }
    ]);
    for city in list(zips):
        print(city)


    # sectors = ["New Brighton"] #"\'E2\\", "\'W1\\", "\'NW1\\", "\'NW2\\", "\'SE2\\", "\'SW2\\", "\'NE1\\", "\'W2\\", "\'SW1\\", "\'NW3\\", "\'SE1\\", "\'E1\\"]
    #
    # for sector in sectors:
    #     jsob = {
    #         "city": sector
    #     }
    #     streets.delete_many(jsob)

if __name__ == "__main__":
    store_num = 'store_'+str(sys.argv[1])
    main(store_num)
