# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 19:25:43 2019

@author: prajkumargoel
"""

#!flask/bin/python
from flask import Flask, jsonify 
from flask import request

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
    return jsonify({'tasks': tasks[0]})

@app.route('/api3', methods=['POST'])
def get_tasks3():

    
#    outText = "Hello There"
#    output = {
#                    "speech": outText,
#                    "displayText": outText,
#                    # "data": data,
#                    # "contextOut": [],
#                    "source": "Dhaval"
#                }

    
#    output =            {
#              "payload": {
#                "google": {
#                  "expectUserResponse": False,
#                  "richResponse": {
#                    "items": [
#                      {
#                        "simpleResponse": {
#                          "textToSpeech": "Hello There"
#                        }
#                      }
#                    ]
#                  }
#                }
#              }
#            }
    input = request.get("body").get("queryResult").get("queryText")
    output = {
                "fulfillmentText"     : "Hello There. API Call Successful using {} webhook".format(input),
                "fulfillmentMessages" : [{"text": {"text":["Hello There. API Call Successful"]}}]
            
            
            }
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)



