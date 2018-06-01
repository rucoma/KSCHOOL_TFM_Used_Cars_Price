#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 19:46:36 2018

@author: rucoma
"""

# Import modules
import pandas as pd
pd.set_option("max_columns", 50)
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn import ensemble
from sklearn.model_selection import train_test_split, KFold
from sklearn import metrics
import warnings
warnings.simplefilter('ignore')
from sklearn.externals import joblib

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
                                      'kilometerCategorical',
                                      #'kilometer000',
                                      'notRepairedDamage',
                                      #'postalCode',
                                      'state',
                                      #'community',
                                      'price'],
                               dtype={'brand': 'str', 
                                      'model': 'str', 
                                      'vehicleType': 'str', 
                                      'gearbox': 'str', 
                                      'yearOfRegistration': np.int64,
                                      'fuelType': 'str',
                                      'powerPS': np.int64,
                                      #'kilometer': np.int64,
                                      'kilometerCategorical': 'str',
                                      #'kilometer000': np.int64,
                                      'notRepairedDamage': 'str',
                                      #'postalCode': 'str',
                                      'state': 'str',
                                      #'community':'str',
                                      'price': np.int64})

# Creation of features dataset
featuresDatasetCars = datasetCarsFinal.copy()
featuresDatasetCars = featuresDatasetCars.drop('price', axis=1)

## Aqui tendriamos que aplicar la metodología de MJosé
# Get dummies
featuresDatasetCarsDummies = pd.get_dummies(featuresDatasetCars)

# Creation of train and test
np.random.seed(42)
train, test = train_test_split(featuresDatasetCarsDummies.index, test_size=.2)

# Crear los datasets
X_train = featuresDatasetCarsDummies.loc[train]
y_train = datasetCarsFinal.loc[train]['price']

X_test = featuresDatasetCarsDummies.loc[test]
y_test = datasetCarsFinal.loc[test]['price']



# Random Forst Regressor
regr = ensemble.RandomForestRegressor(n_jobs=-1,
                                     verbose=1).fit(X_train,
                                              y_train)

# Saving the model
joblib.dump(regr, filename='./output/102_RandomForest.pkl')

# Scores
regr.score(X_train, y_train)
regr.score(X_test, y_test)

# Predictions
pred_train = pd.Series(regr.predict(X_train))
pred_test = pd.Series(regr.predict(X_test))

# Visualization
plt.scatter(y_train, pred_train, alpha=.2)
plt.plot([200, 200000], [200, 200000], color='red')
plt.title('Train data')
plt.xlabel('Real price')
plt.ylabel('Predicted price')

plt.scatter(y_test, pred_test, alpha=.2)
plt.plot([200, 200000], [200, 200000], color='red')
plt.title('Test data')
plt.xlabel('Real price')
plt.ylabel('Predicted price')


# Fine tuning of parameters
paramGrid = {
    'n_estimators': [10, 20, 50, 100],
    'max_depth': list(range(3, 10 + 1)),
    'max_features': [None, 'sqrt'],
}

scores = {}
for max_depth in paramGrid['max_depth']:
    print(max_depth)
    for max_features in paramGrid['max_features']:
        print(max_features)
        rf = ensemble.RandomForestRegressor(
                max_depth=max_depth,
                max_features=max_features,
                oob_score=True,
                warm_start=True,
                n_jobs=-1,
                verbose=1
                )
        for n_estimators in paramGrid['n_estimators']:
            print(n_estimators)
            rf.n_estimators = n_estimators
            scores[(max_depth, max_features, n_estimators)] = rf.fit(X_train, y_train).oob_score_
            
# Getting the maximum score
pd.Series(scores).sort_values(ascending=False).head(10)
max(scores, key=scores.get), max(scores.values())



# Random Forst Regressor final model
regr = ensemble.RandomForestRegressor(n_jobs=-1,
                                     verbose=1,
                                     n_estimators=100,
                                     max_depth=10,
                                     max_features=None).fit(X_train,
                                                      y_train)

# Scores
regr.score(X_train, y_train)
regr.score(X_test, y_test)

# Predictions
pred_train = pd.Series(regr.predict(X_train))
pred_test = pd.Series(regr.predict(X_test))

# Saving the final model
joblib.dump(regr, filename='./output/102_RandomForestFinal.pkl')

## FINISH