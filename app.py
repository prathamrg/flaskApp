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

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

def func1(num1, num2):
    return num1 + num2

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks[1]})

@app.route('/api2', methods=['GET'])
def get_tasks2():
    return jsonify(Response.makeResponse("api2 caled"))

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



