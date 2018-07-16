# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
import matplotlib.pyplot as plt

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

target = datasetCarsFinal['price']

# Create train and test
np.random.seed(42)
train, test = train_test_split(datasetCarsFinal.index, test_size = 0.2)

X_train = datasetCarsFinal.loc[train]
y_train = target.loc[train]

X_test = datasetCarsFinal.loc[test]
y_test = target.loc[test]

df_mapper = DataFrameMapper([('brandModel', preprocessing.LabelEncoder()),
                             ('vehicleType', preprocessing.LabelEncoder()),
                             ('gearbox', preprocessing.LabelEncoder()),
                             ('fuelType', preprocessing.LabelEncoder()),
                             ('kilometerCategorical', preprocessing.LabelEncoder()),
                             ('notRepairedDamage', preprocessing.LabelEncoder()),
                             ('state', preprocessing.LabelEncoder())])
mypipeline = Pipeline([('df_mapper', df_mapper),
                       ('oh', preprocessing.OneHotEncoder()),
                       ('rf', RandomForestRegressor(verbose=1, max_depth=10, max_features='auto', min_samples_leaf=1, min_samples_split=3, n_estimators=50))
                      ])
rf = mypipeline.fit(X_train, y_train)
pred = mypipeline.predict(X_test)

plt.figure(figsize=(6, 4))
plt.scatter(y_test, pred, s=20,alpha=0.1)
plt.title('Estimated Price vs. Real Price. Train dataset')
plt.xlabel('Real Price')
plt.ylabel('Predicted Price')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'y')
plt.tight_layout()