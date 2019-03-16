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



app = Flask(__name__)

@app.route('/test', methods=['POST'])
def testMongo():
    #dict1 = mongoDB.getData("guidebook","restaurants")
    #return jsonify(address=dict1.get('address'),borough=dict1.get('borough'))
    req = request.get_json(silent=True, force=True)
    mongoDB.insertData(req)

    return jsonify(req)

@app.route('/authentication', methods=['POST'])
def authenticate():
    req = request.get_json(silent=True, force=True)
    return jsonify(req)

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

        response = "Since when do you have {}? Today, Yesterday, This Week?".format(primarySymptom)

    elif intent == "SymptomDuration":
        outputContexts = req.get("queryResult").get("outputContexts")
        for outputContext in outputContexts:
            if "primarysymptom-followup" in outputContext.get("name"):
                parameters = outputContext.get("parameters")
                primarySymptom = parameters.get("PrimarySymptom")
                symptomSeverity = parameters.get("SymptomSeverity")
                sleepPattern    = parameters.get("SleepPattern")
                symptomDuration = parameters.get("SymptomDuration")
        response = "You have {0} {1} since {2} and are {3}".format(symptomSeverity,primarySymptom,symptomDuration,sleepPattern)
        params = {
                  "patient_id": 4567,
                  "patient_name":"Jane Doe",
                  "date": str(datetime.utcnow()),
                  "symptom":primarySymptom,
                  "symptom_severity":symptomSeverity,
                  "symptom_duration":symptomDuration,
                  "sleep_pattern":sleepPattern
                }
        mongoDB.insertData(params)






    output = Response.makeResponse(response)
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)



