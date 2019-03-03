# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 13:05:30 2019

@author: prajkumargoel
"""

class Response():
    
    def makeResponse(text):
        return {
                "fulfillmentText"     : text,
                "fulfillmentMessages" : [{"text": {"text":[text]}}]
                
            }