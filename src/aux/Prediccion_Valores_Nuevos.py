#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 11:22:00 2018

@author: rucoma
"""

import pandas as pd
pd.set_option("max_columns", 50)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from collections import OrderedDict, defaultdict
from sklearn.externals import joblib
from sklearn.metrics import r2_score, mean_squared_error

# read csv files
datasetCarsFinal = pd.read_csv('./data/autosFinal.csv',
                               usecols=[
                                      #'brand', 
                                      #'model', 
                                      'brandModel',
                                      'vehicleType', 
                                      'gearbox', 
                                      'yearOfRegistration',
                                      'fuelType',
                                      'powerPS',
                                      'kilometer',
                                      #'kilometerCategorical',
                                      #'kilometer000',
                                      'notRepairedDamage',
                                      #'postalCode',
                                      'state',
                                      #'community',
                                      'price'
                                      ],
                               dtype={
                                      #'brand': 'str', 
                                      #'model': 'str', 
                                      'brandModel': 'str', 
                                      'vehicleType': 'str', 
                                      'gearbox': 'str', 
                                      'yearOfRegistration': np.int64,
                                      'fuelType': 'str',
                                      'powerPS': np.int64,
                                      'kilometer': np.int64,
                                      #'kilometerCategorical': 'str',
                                      #'kilometer000': np.int64,
                                      'notRepairedDamage': 'str',
                                      #'postalCode': 'str',
                                      'state': 'str',
                                      #'community':'str',
                                      'price': np.int64
                                      })

datasetCarsFinal.head()
datasetCarsFinal.columns

target = datasetCarsFinal['price']
numerical = datasetCarsFinal[['yearOfRegistration', 'powerPS', 'kilometer']]
categorical = datasetCarsFinal.drop(['yearOfRegistration', 'powerPS', 'price', 'kilometer'], axis=1)

d = defaultdict(LabelEncoder)
categorical_encoded = categorical.apply(lambda x: d[x.name].fit_transform(x))
datasetCarsFinalConcat = pd.concat([categorical_encoded, numerical], axis=1)

joblib.dump(d, './output/testLabelEncoder.pkl')

#d = joblib.load('./output/carsLabelEncoder.pkl')
bestDecisionTree = joblib.load('./output/bestDecisionTree.pkl')
bestRandomForest = joblib.load('./output/bestRandomForest.pkl')
bestKNN = joblib.load('./output/bestKNN.pkl')
bestBoost = joblib.load('./output/bestBoost.pkl')

d2 = joblib.load('./output/testLabelEncoder.pkl')

newData = pd.DataFrame({'state': ['Bayern', 'Bayern'],
                        'vehicleType': ['cabrio', 'cabrio'],
                        'yearOfRegistration': [2015, 2015],
                        'gearbox': ['manuell', 'manuell'],
                        'powerPS': [90, 50],
                        'fuelType': ['diesel', 'diesel'],
                        'notRepairedDamage': ['ja', 'ja'],
                        'kilometer': [150000, 5000],
                        'brandModel': ['mini clubman', 'mini clubman']})

numericalNew = newData[['yearOfRegistration', 'powerPS', 'kilometer']]
categoricalNew = newData.drop(['yearOfRegistration', 'powerPS', 'kilometer'], axis=1)



newDataEncoded = categoricalNew.apply(lambda x: d2[x.name].transform(x))
newDataEncodedConcat = pd.concat([newDataEncoded, numericalNew], axis=1)

bestDecisionTree.predict(newDataEncodedConcat)
bestRandomForest.predict(newDataEncodedConcat)
bestKNN.predict(newDataEncodedConcat)
bestBoost.predict(newDataEncodedConcat)
