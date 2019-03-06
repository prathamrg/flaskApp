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

@app.route('/api3', methods=['POST'])
def get_tasks3():

    req = request.get_json(silent=True, force=True)
    input = req.get("queryResult").get("queryText")
    
    primarySymptoms = req.get("queryResult").get("parameters").get("PrimarySymptom")
    
    text   = "You have {}".format(primarySymptoms[0])
    output = Response.makeResponse(text)
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)



