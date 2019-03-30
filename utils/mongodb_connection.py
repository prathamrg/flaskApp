import pymongo

class mongoDB():

    def makeConnection():
        client = pymongo.MongoClient("mongodb+srv://pratham:mongodbatpratham95@cluster0-cjgfn.mongodb.net/test?retryWrites=true")
        return client

    def closeConnection(client):
        client.close()

    def sign_up(client, patient_params, dbname="patient_detail", collectionname="patient_metadata"):

        db = client[dbname]
        collection = db[collectionname]

        query = {"patient_id":patient_params["patient_id"]}
        document = collection.find_one(query)

        # if no user with patient_id exisits:
        if document is None:
            collection.insert_one(patient_params)
            return "Your account Has been created! Please sign in with your credentials to start interacting with Virtual Nurse!"

        else:
            return "Sorry. Another user with this patient id already exists. Please try signing up with a unique id"

    def sign_in(client, patient_id, password, dbname="patient_detail", collectionname="patient_metadata"):

        db = client[dbname]
        collection = db[collectionname]

        query = {"patient_id": patient_id}
        document = collection.find_one(query)

        if document.get('patient_id') == patient_id and document.get('password') == password:
            return True, document
        else:
            return False, "username or password invalid. Please try again"

    def lookup_patient(client, patient_id, dbname="patient_detail", collectionname="patient_metadata"):

        db = client[dbname]
        collection = db[collectionname]

        query = {"patient_id": patient_id}
        document = collection.find_one(query)

        return document

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






