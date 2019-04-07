# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 19:25:43 2019

@author: prajkumargoel
"""

#!flask/bin/python
from flask import Flask, jsonify, session, g
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
#app.secret_key = '@^@vjvjgufr767t7796w221697643uknklucfgcvjbvfvbjhkgdcj57655744332'
#app.secret_key = 'ceb212e796ee40d6b35c9cc171c34c3a'

app.secret_key = '#$#$!#aknadjkandk@%$%21697643uknklucfgcvjbvfvbjhkgdcj5765as89080'


@app.before_request
def before_request():
    #g.patient_id = None
    #g.patient_name = None
    #g.patient_age = None
    #g.patient_gender = None

    if 'patient_id' in session:
        g.patient_id = session['patient_id']
    if 'patient_name' in session:
        g.patient_name = session['patient_name']
    if 'patient_age' in session:
        g.patient_age = session['patient_age']
    if 'patient_gender' in session:
        g.patient_gender = session['patient_gender']

@app.route('/get_session', methods=['GET'])
def get_session():

    res = {
        "patient_id" : session['patient_id'],
        "patient_name": session['patient_name'],
        "patient_age": session['patient_age'],
        "patient_gender": session['patient_gender']
    }

    # return jsonify([g.patient_id,
    # g.patient_name,
    # g.patient_age,
    # g.patient_gender])

    return jsonify(res)

@app.route('/get_latest_detail', methods=['GET'])
def get_latest_detail():
    req = request.get_json(silent=True, force=True)

    with open(os.path.dirname(os.path.realpath(__file__)) + '/temp/temp.json', 'r') as tmpfile:
        patient_metadata = json.load(tmpfile)

    client = mongoDB.makeConnection()
    patient_detail = mongoDB.getPatientData(client, patient_id=patient_metadata['patient_id'])
    mongoDB.closeConnection(client)

    # predict overall condition based on latest survey
    if patient_detail is not None:
        latest = patient_detail.get(sorted(patient_detail.keys(), reverse=True)[2])
        return jsonify(latest)
    else:
        return jsonify("No saved records found")

@app.route('/get_hcp_detail', methods=['POST'])
def get_hcp_detail():

    req = request.get_json(silent=True, force=True)

    latitude = req['latitude']
    longitude = req['longitude']

    hcp_name = "Pratham"
    hcp_number = "+918758085009"
    hcp_email = "prathamgoel95@gmail.com"

    res = {"hcp_name": hcp_name, "hcp_number": hcp_number, "hcp_email":hcp_email}
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

        session.permanent = True

        g.patient_id = obj.get('patient_id')
        g.patient_name = obj.get('patient_name')
        g.patient_age = obj.get('patient_age')
        g.patient_gender = obj.get('patient_gender')

        patient_metadata = {}
        patient_metadata['patient_id'] = obj.get('patient_id')
        patient_metadata['patient_name'] = obj.get('patient_name')
        patient_metadata['patient_age'] = obj.get('patient_age')
        patient_metadata['patient_gender'] = obj.get('patient_gender')

        with open(os.path.dirname(os.path.realpath(__file__))+'/temp/temp.json', 'w') as tmpfile:
            json.dump(patient_metadata,tmpfile)



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

    with open(os.path.dirname(os.path.realpath(__file__)) + '/temp/temp.json', 'r') as tmpfile:
        patient_metadata = json.load(tmpfile)

    client = mongoDB.makeConnection()
    patient_detail = mongoDB.getPatientData(client, patient_id=patient_metadata['patient_id'])
    mongoDB.closeConnection(client)

    # predict overall condition based on latest survey

    latest = patient_detail.get(sorted(patient_detail.keys(), reverse=True)[2])
    print(latest)

    # common parameters
    age = patient_metadata["patient_age"]
    gender = dictionary_preprocess.gender_mapping.get(patient_metadata["patient_gender"])

    # parameters for primary symptom flow
    severity = dictionary_preprocess.severity_mapping.get(latest.get("symptom_severity")) if dictionary_preprocess.severity_mapping.get(latest.get("symptom_severity")) is not None else 1
    duration = dictionary_preprocess.duration_mapping.get(latest.get("symptom_duration")) if dictionary_preprocess.duration_mapping.get(latest.get("symptom_duration")) is not None else 1
    sleep = dictionary_preprocess.sleep_mapping.get(latest.get("sleep_pattern")) if dictionary_preprocess.sleep_mapping.get(latest.get("sleep_pattern")) is not None else 1
    symptom = dictionary_preprocess.symptom_mapping.get(latest.get("symptom")) if dictionary_preprocess.symptom_mapping.get(latest.get("symptom")) is not None else 1

    # parameters for accident flow
    accident_severity = dictionary_preprocess.severity_mapping.get(latest.get("accident_severity")) if dictionary_preprocess.severity_mapping.get(latest.get("accident_severity")) is not None else 1
    accident_duration = dictionary_preprocess.duration_mapping.get(latest.get("accident_duration")) if dictionary_preprocess.duration_mapping.get(latest.get("accident_duration")) is not None else 1
    accident_part = dictionary_preprocess.part_mapping.get(latest.get("accident_part")) if dictionary_preprocess.part_mapping.get(latest.get("accident_part")) is not None else 1
    accident = dictionary_preprocess.accident_mapping.get(latest.get("accident")) if dictionary_preprocess.accident_mapping.get(latest.get("accident")) is not None else 1


    # prepare symptom or accident feature set:
    if "accident" in latest:
        #data = [accident_severity,accident_duration,accident_part,accident]
        data = [accident, age, gender, accident_part, accident_severity, accident_duration]
        pickle_file = 'finalized_model_accident.pkl'
        #add age, gender
    else:
        #data = [severity,duration,sleep,symptom]
        data = [symptom, age, gender, sleep, severity, duration]
        pickle_file = 'finalized_model_symptom.pkl'
        #add age, gender
    print(data)

    #postman testing
    #decision_tree_clf = pickle.load(open(os.path.dirname(os.path.realpath(__file__))+'\\models\\decision_tree_model.sav','rb'))

    #heroku deployment
    #decision_tree_clf = pickle.load(open(os.path.dirname(os.path.realpath(__file__))+'/models/decision_tree_model.sav','rb'))
    decision_tree_clf = pickle.load(open(os.path.dirname(os.path.realpath(__file__))+'/models/'+pickle_file,'rb'))
    patient_health = ML.predict(decision_tree_clf,data)
    print(patient_health)
    emails.send_email(payload=patient_detail, patient_health=patient_health)

    return jsonify("Patient Health is {}. Email sent to HCP".format(patient_health))
    #return jsonify(latest)


@app.route('/dialogflow_webhook', methods=['POST'])
def processRequest():

    req = request.get_json(silent=True, force=True)
    intent = req.get("queryResult").get("intent").get("displayName")

    keys = session.keys()


    # Greetings
    if intent == "Welcome":

        patient_metadata = {}

        with open(os.path.dirname(os.path.realpath(__file__))+'/temp/temp.json', 'r') as tmpfile:
            patient_metadata = json.load(tmpfile)

        response = '''Hello {}, I am your Virtual Nurse. 
                    I can help you with advice on first aid for your symptom or accident by asking you a few simple questions. 
                    Or I could call up your nearest doctor. Please let me know what is your primary symptom or accident
                    '''.format(str(patient_metadata['patient_name']))

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

        with open(os.path.dirname(os.path.realpath(__file__))+'/temp/temp.json', 'r') as tmpfile:
            patient_metadata = json.load(tmpfile)
        params = {
            "patient_id": patient_metadata['patient_id'],
            "patient_name": patient_metadata['patient_name'],
            "patient_age": patient_metadata['patient_age'],
            "patient_gender": patient_metadata['patient_gender'],
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


    elif intent == "ConfirmSendAccidentDetails":
        outputContexts = req.get("queryResult").get("outputContexts")
        for outputContext in outputContexts:
            if "accidentsymptom-followup" in outputContext.get("name"):
                parameters = outputContext.get("parameters")
                AccidentSymptom = parameters.get("AccidentSymptom")
                AccidentSeverity = parameters.get("SymptomSeverity")
                AccidentPart    = parameters.get("AccidentPart")
                AccidentDuration = parameters.get("SymptomDuration")

        with open(os.path.dirname(os.path.realpath(__file__))+'/temp/temp.json', 'r') as tmpfile:
            patient_metadata = json.load(tmpfile)

        params = {
                  "patient_id": patient_metadata['patient_id'],
                  "patient_name": patient_metadata['patient_name'],
                  "patient_age": patient_metadata['patient_age'],
                  "patient_gender": patient_metadata['patient_gender'],
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



