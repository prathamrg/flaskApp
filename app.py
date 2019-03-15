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



app = Flask(__name__)

@app.route('/fetch_data', methods=['GET'])
def getData():
    dict1 = mongoDB.getData("guidebook","restaurants")
    return jsonify(address=dict1.get('address'),borough=dict1.get('borough'))

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
        response = "Alright. What is the severity of your {}? Low, Moderate or High?".format(primarySymptoms[0])
    
    elif intent == "SymptomSeverity":

        response = "How do you feel of late? Tired or Restless?"

    elif intent == "SleepPattern":

        outputContexts = req.get("queryResult").get("outputContexts")
        for outputContext in outputContexts:
            if "primarysymptom-followup" in outputContext.get("name"):
                parameters = outputContext.get("parameters")
                primarySymptoms = parameters.get("PrimarySymptom")
                symptomSeverity = parameters.get("SymptomSeverity")
                sleepPattern    = parameters.get("SleepPattern")
        response = "You have {0} {1} and are {2}".format(symptomSeverity,primarySymptoms[0],sleepPattern)

    output = Response.makeResponse(response)
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)



