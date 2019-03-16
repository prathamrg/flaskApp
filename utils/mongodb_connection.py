import pymongo

class mongoDB():


    def getData(params, dbname="Medical_Database", collectionname="Symptom_FirstAid"):

        client = pymongo.MongoClient("mongodb+srv://pratham:mongodbatpratham95@cluster0-cjgfn.mongodb.net/test?retryWrites=true")
        db = client[dbname]
        collection = db[collectionname]

        symptom = params.get("symptoms")
        query = {"symptom":symptom}

        document = collection.find_one(query)
        first_aid = document.get("first-aid")
        #dictionary = collection.find_one()
        client.close()
        return first_aid

    def insertData(params, dbname="patient_detail", collectionname="patient_detail"):

        client = pymongo.MongoClient(
        "mongodb+srv://pratham:mongodbatpratham95@cluster0-cjgfn.mongodb.net/test?retryWrites=true")
        db = client[dbname]
        collection = db[collectionname]

        query = {"patient_id":params.get("patient_id")}

        update = {"$set": {"patient_name":params.get("patient_name"),
                           "patient_history_{}".format(params.get("date")):
                                                   {
                                                    "symptom":params.get("symptom"),
                                                    "symptom_severity": params.get("symptom_severity"),
                                                    "symptom_duration": params.get("symptom_duration"),
                                                    "sleep_pattern": params.get("sleep_pattern")
                                                   }}}

        collection.update(query,update,upsert=True)
        client.close()





