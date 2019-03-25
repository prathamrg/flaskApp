# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 19:25:43 2019

@author: prajkumargoel
"""

#!flask/bin/python
from flask import Flask, jsonify 
from flask import request
from utils.mongodb_connection import mongoDB
from utils.helper import Response
import json
from _datetime import datetime
from utils import emails



app = Flask(__name__)

@app.route('/test', methods=['POST'])
def testMongo():


    req = request.get_json(silent=True, force=True)

    res = mongoDB.getData(req)
    #mongoDB.insertData(req)

    return jsonify(res)

@app.route('/send_email', methods=['POST'])
def send_email():

    req = request.get_json(silent=True, force=True)

    client = mongoDB.makeConnection()
    patient_detail = mongoDB.getPatientData(client, patient_id=4567)
    mongoDB.closeConnection(client)
    emails.send_email(message=patient_detail, patient_health="Severe")

    return jsonify("Email sent to HCP")

@app.route('/dialogflow_webhook', methods=['POST'])
def processRequest():

    req = request.get_json(silent=True, force=True)
    intent = req.get("queryResult").get("intent").get("displayName")

    if intent == "PrimarySymptom":

        primarySymptoms = req.get("queryResult").get("parameters").get("PrimarySymptom")
        response = "Alright. What is the severity of your {}? Low, Moderate or High?".format(primarySymptoms)
    
    elif intent == "SymptomSeverity":

        response = "How do you feel of late? Tired or Restless?"

    elif intent == "SleepPattern":

        outputContexts = req.get("queryResult").get("outputContexts")
        for outputContext in outputContexts:
            if "primarysymptom-followup" in outputContext.get("name"):
                parameters = outputContext.get("parameters")
                primarySymptom = parameters.get("PrimarySymptom")
                symptomSeverity = parameters.get("SymptomSeverity")
                sleepPattern    = parameters.get("SleepPattern")

        response = "Since when do you have {}?".format(primarySymptom)

    elif intent == "SymptomDuration":
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

        response = "Thanks for providing the information. Since you have {0} {1} since {2} and are {3}, I suggest you to take the following course of preliminary action: {4}. Do you want me to send your details to the nearest HCP?".format(symptomSeverity,primarySymptom,symptomDuration,sleepPattern,first_aid)

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

        response = "I have shared your concerns with your nearest HCP who shall revert to you shortly"

    output = Response.makeResponse(response)
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)



