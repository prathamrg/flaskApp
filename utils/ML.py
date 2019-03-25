# Run this program on your local python
# interpreter, provided you have installed
# the required libraries.

# Importing the required packages
import numpy as np
# import pandas as pd
# from sklearn.metrics import confusion_matrix
# #from sklearn.cross_validation import train_test_split
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import classification_report


def predict(model,data):
    return model.predict(np.asarray(data))