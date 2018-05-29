#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 19:46:36 2018

@author: rucoma
"""

# Import modules
import pandas as pd
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
                                      'postalCode',
                                      'state',
                                      'community',
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
                                      'postalCode': 'str',
                                      'state': 'str',
                                      'community':'str',
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



# Random Forst Regressor (tarda 1 hora)
regr = ensemble.RandomForestRegressor().fit(featuresDatasetCarsDummies.loc[train],
                                     datasetCarsFinal.price[train],
                                     n_jobs=-1)

# Saving the model
joblib.dump(regr, filename='./output/102_RandomForest.pkl')

# Scores
regr.score(featuresDatasetCarsDummies.loc[train], datasetCarsFinal.price[train])
regr.score(featuresDatasetCarsDummies.loc[test], datasetCarsFinal.price[test])

# Predictions

pred_train = pd.Series(regr.predict(featuresDatasetCarsDummies.loc[train]))

pred_test = pd.Series(regr.predict(featuresDatasetCarsDummies.loc[test]), index=datasetCarsFinal.index)

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
                warm_start=True
                )
        for n_estimators in paramGrid['n_estimators']:
            print(n_estimators)
            rf.n_estimators = n_estimators
            scores[(max_depth, max_features, n_estimators)] = rf.fit(featuresDatasetCarsDummies, datasetCarsFinal.price).oob_score_
            
# Getting the maximum score
pd.Series(scores).sort_values(ascending=False).head(10)
max(scores, key=scores.get), max(scores.values())

# Confusion matrix
metrics.confusion_matrix(datasetCarsFinal.price[test], pred[test])
