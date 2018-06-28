#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 22:22:18 2018

@author: rucoma
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn import ensemble
from sklearn import preprocessing
from sklearn import neighbors
from collections import defaultdict
from sklearn.model_selection import train_test_split


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
                                      #'kilometer',
                                      'kilometerCategorical',
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
                                      #'kilometer': np.int64,
                                      'kilometerCategorical': 'str',
                                      #'kilometer000': np.int64,
                                      'notRepairedDamage': 'str',
                                      #'postalCode': 'str',
                                      'state': 'str',
                                      #'community':'str',
                                      'price': np.int64
                                      })

# Split dataset into target, numerical and categorical features
target = datasetCarsFinal['price']
numerical = datasetCarsFinal[['yearOfRegistration', 'powerPS']]
categorical = datasetCarsFinal.drop(['yearOfRegistration', 'powerPS', 'price'], axis=1)

# Encoding categorical variables and merging with numerical
d = defaultdict(preprocessing.LabelEncoder)
categorical_encoded = categorical.apply(lambda x: d[x.name].fit_transform(x))
datasetCarsFinalConcat = pd.concat([categorical_encoded, numerical], axis=1)

# Create train and test
np.random.seed(42)
train, test = train_test_split(datasetCarsFinal.index, test_size = 0.2)

X_train = datasetCarsFinalConcat.loc[train]
y_train = target.loc[train]

X_test = datasetCarsFinalConcat.loc[test]
y_test = target.loc[test]

X_train.shape, y_train.shape 
X_test.shape, y_test.shape 

'''
Three methods
'''

dt = tree.DecisionTreeRegressor().fit(X_train, y_train)
rf = ensemble.RandomForestRegressor().fit(X_train, y_train)
gb = ensemble.GradientBoostingRegressor(n_estimators=500).fit(X_train, y_train)
kn = neighbors.KNeighborsRegressor().fit(X_train, y_train)

(
 dt.score(X_test, y_test),
 rf.score(X_test, y_test),
 gb.score(X_test, y_test),
 kn.score(X_test, y_test)
 )

'''
Gradient Boosting tuning
'''

np.random.seed(123)
scores = {}

gb = None

for n_estimators in [1, 5, 10, 20, 50, 100, 200, 500]:
    print(n_estimators)
    if gb is None:
        gb = ensemble.GradientBoostingRegressor(n_estimators=n_estimators)
    else:
        gb.n_estimators = n_estimators
    gb = gb.fit(X_train, y_train)
    scores[n_estimators] = gb.score(X_test, y_test)
    
pd.Series(scores).plot()
plt.axhline(dt.score(X_test, y_test), linestyle='dashed', color='red')
plt.axhline(rf.score(X_test, y_test), linestyle='dashed', color='green')