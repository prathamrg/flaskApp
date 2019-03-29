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
app.secret_key = b'_##3@#rt^1~8-5#y2L"F4Q8z'

@app.route('/get_session_test', methods=['GET'])
def get_session_test():

    res = {
        "patient_id" : session['patient_id'],
        "patient_name": session['patient_name'],
        "patient_age": session['patient_age'],
        "patient_gender": session['patient_gender']
    }

    return jsonify(res)

@app.route('/sign_up', methods=['POST'])
def sign_up():
    req = request.get_json(silent=True, force=True)

    patient_params = {
        "patient_name" : req.get('patient_name'),
        "patient_id" : req.get('patient_id'),
        "password" : req.get('password'),
        "patient_age" : req.get('patient_age'),
        "patient_gender" : req.get('patient_gender')
    }
    client = mongoDB.makeConnection()
    res = mongoDB.sign_up(client,patient_params)
    mongoDB.closeConnection(client)

    return jsonify(res)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    req = request.get_json(silent=True, force=True)

    patient_id = req.get('patient_id')
    password = req.get('password')

    client = mongoDB.makeConnection()
    is_login_success, obj = mongoDB.sign_in(client,patient_id,password)
    mongoDB.closeConnection(client)

    if is_login_success is False:
        return jsonify(obj)
    else:
        session['patient_id'] = obj.get('patient_id')
        session['patient_name'] = obj.get('patient_name')
        session['patient_age'] = obj.get('patient_age')
        session['patient_gender'] = obj.get('patient_gender')
        return jsonify("Login Successful! You may now interact with Virtual Nurse")

@app.route('/sign_out', methods=['GET'])
def sign_out():
    session.pop('patient_id',None)
    session.pop('password',None)
    session.pop('patient_age',None)
    session.pop('patient_gender',None)

    return jsonify("You have successfully logged out of Virtual Nurse")


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
                sleepPattern = parameters.get("SleepPattern")
                symptomDuration = parameters.get("SymptomDuration")

        client = mongoDB.makeConnection()
        first_aid = mongoDB.getData(client,primarySymptom)
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
            "patient_id": session['patient_id'],
            "patient_name": session['patient_name'],
            "patient_age": session['patient_age'],
            "patient_gender": session['patient_gender'],
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



        client = mongoDB.makeConnection()
        first_aid = mongoDB.getData(client,AccidentSymptom)
        #mongoDB.insertData(client,params)
        mongoDB.closeConnection(client)

        response = "Thanks for providing the information. I suggest you to take the following course of preliminary action: {}. Do you want me to save your details?".format(first_aid)


    elif intent == "ConfirmSendAccidentDetail":
        outputContexts = req.get("queryResult").get("outputContexts")
        for outputContext in outputContexts:
            if "accidentsymptom-followup" in outputContext.get("name"):
                parameters = outputContext.get("parameters")
                AccidentSymptom = parameters.get("AccidentSymptom")
                AccidentSeverity = parameters.get("SymptomSeverity")
                AccidentPart    = parameters.get("AccidentPart")
                AccidentDuration = parameters.get("SymptomDuration")

        params = {
                  "patient_id": session['patient_id'],
                  "patient_name": session['patient_name'],
                  "patient_age": session['patient_age'],
                  "patient_gender": session['patient_gender'],
                  "date": str(datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')),
                  "accident":AccidentSymptom,
                  "accident_severity":AccidentSeverity,
                  "accident_duration":AccidentDuration,
                  "accident_part":AccidentPart
                }

        client = mongoDB.makeConnection()
        #first_aid = mongoDB.getData(client,AccidentSymptom)
        mongoDB.insertData(client,params, type="accident")
        mongoDB.closeConnection(client)

        response = "Your details have been saved. Please press the send button if you wish to send a notification to the nearest HCP with your details"



    output = Response.makeResponse(response)
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)



