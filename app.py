# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 19:25:43 2019

@author: prajkumargoel
"""

#!flask/bin/python
from flask import Flask, jsonify, session
from flask import request
from utils.mongodb_connection import mongoDB
from utils.helper import Response
import json
from _datetime import datetime
from utils import emails
from utils import ML
from data import dictionary_preprocess
import pickle
import os



app = Flask(__name__)

@app.route('/test', methods=['POST'])
def testMongo():


    req = request.get_json(silent=True, force=True)

    #res = mongoDB.getData(req)
    #mongoDB.insertData(req)

    return jsonify(ML.test())

@app.route('/send_email', methods=['POST'])
def send_email():

    req = request.get_json(silent=True, force=True)

    client = mongoDB.makeConnection()
    patient_detail = mongoDB.getPatientData(client, patient_id=4567)
    mongoDB.closeConnection(client)

    # predict overall condition based on latest survey

    latest = patient_detail.get(sorted(patient_detail.keys(), reverse=True)[2])
    print(latest)

    severity = dictionary_preprocess.severity_mapping.get(latest["symptom_severity"]) if dictionary_preprocess.severity_mapping.get(latest["symptom_severity"]) is not None else 1
    duration = dictionary_preprocess.duration_mapping.get(latest["symptom_duration"]) if dictionary_preprocess.duration_mapping.get(latest["symptom_duration"]) is not None else 1
    sleep = dictionary_preprocess.sleep_mapping.get(latest["sleep_pattern"]) if dictionary_preprocess.sleep_mapping.get(latest["sleep_pattern"]) is not None else 1
    symptom = dictionary_preprocess.symptom_mapping.get(latest["symptom"]) if dictionary_preprocess.symptom_mapping.get(latest["symptom"]) is not None else 1

    data = [severity,duration,sleep,symptom]
    print(data)

    #postman testing
    #decision_tree_clf = pickle.load(open(os.path.dirname(os.path.realpath(__file__))+'\\models\\decision_tree_model.sav','rb'))

    #heroku deployment
    decision_tree_clf = pickle.load(open(os.path.dirname(os.path.realpath(__file__))+'/models/decision_tree_model.sav','rb'))
    patient_health = ML.predict(decision_tree_clf,data)
    print(patient_health)
    emails.send_email(payload=patient_detail, patient_health=patient_health)

    return jsonify("Patient Health is {}. Email sent to HCP".format(patient_health))
    #return jsonify(latest)


@app.route('/dialogflow_webhook', methods=['POST'])
def processRequest():

    req = request.get_json(silent=True, force=True)
    intent = req.get("queryResult").get("intent").get("displayName")

    # Primary Symptom Follow-Up Flow:
    if intent == "SymptomDuration":
        outputContexts = req.get("queryResult").get("outputContexts")
        for outputContext in outputContexts:
            if "primarysymptom-followup" in outputContext.get("name"):
                parameters = outputContext.get("parameters")
                primarySymptom = parameters.get("PrimarySymptom")
                symptomSeverity = parameters.get("SymptomSeverity")
                sleepPattern    = parameters.get("SleepPattern")
                symptomDuration = parameters.get("SymptomDuration")

        params = {
                  "patient_id": 4567,
                  "patient_name":"Jane Doe",
                  "date": str(datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')),
                  "symptom":primarySymptom,
                  "symptom_severity":symptomSeverity,
                  "symptom_duration":symptomDuration,
                  "sleep_pattern":sleepPattern
                }

        client = mongoDB.makeConnection()
        first_aid = mongoDB.getData(client,params)
        #mongoDB.insertData(client,params)
        mongoDB.closeConnection(client)

        response = "Thanks for providing the information. Since you have {0} {1} since {2} and are {3}, I suggest you to take the following course of preliminary action: {4}. Do you want me to save your details?".format(symptomSeverity,primarySymptom,symptomDuration,sleepPattern,first_aid)

    elif intent == "ConfirmSend":

        outputContexts = req.get("queryResult").get("outputContexts")
        for outputContext in outputContexts:
            if "primarysymptom-followup" in outputContext.get("name"):
                parameters = outputContext.get("parameters")
                primarySymptom = parameters.get("PrimarySymptom")
                symptomSeverity = parameters.get("SymptomSeverity")
                sleepPattern = parameters.get("SleepPattern")
                symptomDuration = parameters.get("SymptomDuration")

        params = {
            "patient_id": 4567,
            "patient_name": "Jane Doe",
            "date": str(datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')),
            "symptom": primarySymptom,
            "symptom_severity": symptomSeverity,
            "symptom_duration": symptomDuration,
            "sleep_pattern": sleepPattern
        }

        client = mongoDB.makeConnection()
        mongoDB.insertData(client,params)
        mongoDB.closeConnection(client)

        response = "Your details have been saved. Please press the send button if you wish to send a notification to the nearest HCP with your details"

    # Accident Follow-Up Flow:
    elif intent == "AccidentDuration":
        outputContexts = req.get("queryResult").get("outputContexts")
        for outputContext in outputContexts:
            if "accidentsymptom-followup" in outputContext.get("name"):
                parameters = outputContext.get("parameters")
                AccidentSymptom = parameters.get("AccidentSymptom")
                AccidentSeverity = parameters.get("SymptomSeverity")
                AccidentPart    = parameters.get("AccidentPart")
                AccidentDuration = parameters.get("SymptomDuration")

        params = {
                  "patient_id": 4567,
                  "patient_name":"Jane Doe",
                  "date": str(datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')),
                  "symptom":AccidentSymptom,
                  "accident_severity":AccidentSeverity,
                  "accident_duration":AccidentDuration,
                  "accident_part":AccidentPart
                }

        client = mongoDB.makeConnection()
        first_aid = mongoDB.getData(client,params)
        #mongoDB.insertData(client,params)
        mongoDB.closeConnection(client)

        response = "Thanks for providing the information. I suggest you to take the following course of preliminary action: {}. Do you want me to save your details?".format(first_aid)




    output = Response.makeResponse(response)
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)



