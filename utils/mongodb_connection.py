import pymongo

class mongoDB():

    def makeConnection():
        client = pymongo.MongoClient("mongodb+srv://pratham:mongodbatpratham95@cluster0-cjgfn.mongodb.net/test?retryWrites=true")
        return client

    def closeConnection(client):
        client.close()



    def getPatientData(client, patient_id, dbname="patient_detail", collectionname="patient_detail"):

        #client = pymongo.MongoClient("mongodb+srv://pratham:mongodbatpratham95@cluster0-cjgfn.mongodb.net/test?retryWrites=true")
        db = client[dbname]
        collection = db[collectionname]


        query = {"patient_id":patient_id}

        document = collection.find_one(query)

        client.close()
        return document




    def getData(client, symptom, dbname="Medical_Database", collectionname="Symptom_FirstAid"):

        #client = pymongo.MongoClient("mongodb+srv://pratham:mongodbatpratham95@cluster0-cjgfn.mongodb.net/test?retryWrites=true")
        db = client[dbname]
        collection = db[collectionname]

        #symptom = params.get("symptom")
        query = {"symptom":symptom}

        document = collection.find_one(query)
        first_aid = document.get("first-aid")
        #dictionary = collection.find_one()
        client.close()
        return first_aid

    def insertData(client, params, dbname="patient_detail", collectionname="patient_detail", type="symptom"):

        #client = pymongo.MongoClient("mongodb+srv://pratham:mongodbatpratham95@cluster0-cjgfn.mongodb.net/test?retryWrites=true")
        db = client[dbname]
        collection = db[collectionname]

        query = {"patient_id":params.get("patient_id")}

        if type=="symptom":
            update = {"$set": {"patient_name":params.get("patient_name"),
                               "patient_history_{}".format(params.get("date")):
                                                       {
                                                        "symptom":params.get("symptom"),
                                                        "symptom_severity": params.get("symptom_severity"),
                                                        "symptom_duration": params.get("symptom_duration"),
                                                        "sleep_pattern": params.get("sleep_pattern")
                                                       }}}

            collection.update(query,update,upsert=True)

        elif type=="accident":
            update = {"$set": {"patient_name": params.get("patient_name"),
                               "patient_history_{}".format(params.get("date")):
                                   {
                                       "accident": params.get("accident"),
                                       "accident_severity": params.get("accident_severity"),
                                       "accident_duration": params.get("accident_duration"),
                                       "accident_part": params.get("accident_part")
                                   }}}

            collection.update(query, update, upsert=True)

        client.close()






