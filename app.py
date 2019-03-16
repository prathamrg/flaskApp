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


    req = request.get_json(silent=True, force=True)

    res = mongoDB.getData(req)
    #mongoDB.insertData(req)

    return jsonify(res)

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
        mongoDB.insertData(client,params)
        first_aid = mongoDB.getData(client,params)
        mongoDB.closeConnection(client)

        response = "Thanks for providing the information. Since you have {0} {1} since {2} and are {3}, I suggest you to take the following course of preliminary action: {4}".format(symptomSeverity,primarySymptom,symptomDuration,sleepPattern,first_aid)







    output = Response.makeResponse(response)
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)



