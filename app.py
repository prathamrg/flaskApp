# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 19:25:43 2019

@author: prajkumargoel
"""

#!flask/bin/python
from flask import Flask, jsonify 
from flask import request
from utils.helper import *



app = Flask(__name__)



@app.route('/authentication', methods=['POST'])
def authenticate():
    req = request.get_json(silent=True, force=True)
    return jsonify(req)

@app.route('/dialogflow_webhook', methods=['POST'])
def processRequest():

    req = request.get_json(silent=True, force=True)
    intent = req.get("intent").get("displayName")

    if intent == "PrimarySymptom":

        primarySymptoms = req.get("queryResult").get("parameters").get("PrimarySymptom")
        response = "Alright. What is the severity of your {}".format(primarySymptoms[0])
    
    elif intent == "SymptomSeverity":

        symptomSeverity = req.get("queryResult").get("parameters").get("SymptomSeverity")
        response = "How do you feel right now? Tired or Restless?"

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



