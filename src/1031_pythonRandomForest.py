#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 22:18:17 2018

@author: rucoma
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn import metrics
import warnings
warnings.simplefilter('ignore')

# read csv files
datasetCarsFinal = pd.read_csv('./data/autosFinal.csv',
                               usecols=['brand', 
                                      'model', 
                                      'vehicleType', 
                                      'gearbox', 
                                      'yearOfRegistration',
                                      'fuelType',
                                      'powerPS',
                                      #'kilometer',
                                      'kilometerCat',
                                      #'kilometer000',
                                      'notRepairedDamage',
                                      #'postalCode',
                                      'state',
                                      'price'],
                               dtype={'brand': 'str', 
                                      'model': 'str', 
                                      'vehicleType': 'str', 
                                      'gearbox': 'str', 
                                      'yearOfRegistration': np.int64,
                                      'fuelType': 'str',
                                      'powerPS': np.int64,
                                      #'kilometer': np.int64,
                                      'kilometerCat': 'str',
                                      #'kilometer000': np.int64,
                                      'notRepairedDamage': 'str',
                                      #'postalCode': 'str',
                                      'state': 'str',
                                      'price': np.int64})
datasetCarsFinal.columns
datasetCarsFinal.head()

# Getting dummies
datasetCarsFinalDummy = pd.get_dummies(datasetCarsFinal)

# Create train and test
np.random.seed(42)
X = datasetCarsFinalDummy.drop(['price'], axis=1)
y = datasetCarsFinalDummy['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8)

# Instantiate the model and fit the model into train set
model = RandomForestRegressor(oob_score=True).fit(X_train, y_train)

model.score(X_train, y_train)
model.score(X_test, y_test)

y_pred = model.predict(X)
y_pred2 = pd.Series(model.predict(X), index=datasetCarsFinalDummy.index) #Así lo convertimos en un data frame igual que y

#Charting results
plt.scatter(datasetCarsFinalDummy.price, y_pred2, alpha=.1)

metrics.mean_squared_error(y_train, model.oob_prediction_)
metrics.mean_absolute_error(y_train, model.oob_prediction_)

#plt.figure(figsize=(6, 4))
#plt.scatter(y_test, y_pred, s=20,alpha=0.1)
#plt.title('Estimated Price vs. Real Price')
#plt.xlabel('Real Price')
#plt.ylabel('Predicted Price')
#
#plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'y')
#plt.tight_layout()

param_grid = {
        'n_estimators': [10, 20, 50, 100],
        'max_depth': list(range(3, 10 + 1)),
        'max_features': [None]}

scores = {}
for max_depth in param_grid['max_depth']:
    print(max_depth)
    for max_features in param_grid['max_features']:
        print(max_features)
        rf = RandomForestRegressor(max_depth=max_depth,
                                   max_features=max_features,
                                   oob_score=True,
                                   warm_start=True)
        for n_estimators in param_grid['n_estimators']:
            rf.n_estimators = n_estimators
            scores[(max_depth, max_features, n_estimators)] = rf.fit(X, y).oob_score_
            
modelFinal = RandomForestRegressor(max_depth=10,
                                   max_features=None,
                                   n_estimators=100,
                                   oob_score=True).fit(X, y)
modelFinal.oob_score_

metrics.mean_squared_error(y, modelFinal.oob_prediction_)
metrics.mean_absolute_error(y, modelFinal.oob_prediction_)
