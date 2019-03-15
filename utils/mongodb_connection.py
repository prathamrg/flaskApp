import pymongo

class mongoDB():


    def getData(dbname, collectionname):
        #dbname = "guidebook"
        #collectionname = "restaurants"
        client = pymongo.MongoClient("mongodb+srv://pratham:mongodbatpratham95@cluster0-cjgfn.mongodb.net/test?retryWrites=true")
        db = client[dbname]
        collection = db[collectionname]

        #collection.database
        dictionary = collection.find_one()
        #print(collection.find_one())
        client.close()
        return dictionary
