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
    #key   = request.json.get('key')
    #value = func1(request.json.get('value'),3)
    #return jsonify({key: value})
	return jsonify(request.json)

if __name__ == '__main__':
    app.run(debug=True)



