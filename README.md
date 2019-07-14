<b>Use case</b>

This repository contains the back-end python code for an android based rural healthcare app - Virtual Nurse
This app is targeted towards people in rural India for quick reporting and diagnosis of their medical symptoms/accidents

The app allows users to communicate with its chatbot that provides first-aid suggestions to the user's medical problems.
Additionally, based on the collected user's responses on a few simple follow-up questions, the app runs an ML model to predict 
the overall criticality of the patient and accordingly sends out alerts to the nearby health care practitioner


<b>High Level Architecture Stack is as follows</b>:

Android App Interface built using React Native <---> Google Dialogflow <---> Flask Web Application hosted on Heroku <---> MongoDB Atlas

Data flow is acheived using REST APIs built using Flask and hosted on a gunicorn server on Heroku. Chatbot interaction model is built
using Google Dialogflow.

ML model is a Decision Tree Classifier built using scikit-learn, 
pre-trained on mocked-up data (due to difficulty in access of healthcare data) and pickeled

Rationale behind using MongoDB as the data store is to make it horizontally scalable for each user

Additionally, an interactive, real-time dashboard is buit on the app-user data collected from this.
Link to dashboard: https://vndashboard.herokuapp.com/
Github Link: 

This dashboard is useful for rural health officers to derive interesting insights about the app-users (people of his rural constituency) like:
1. Which is the most common symptom ocurring in children aged 1 to 10 
2. What kind of accidents are most common for women, (for e.g. snake bites, suggesting a need for installing more street-lights in the area)



