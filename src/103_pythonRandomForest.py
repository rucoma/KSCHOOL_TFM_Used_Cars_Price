#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 23:28:03 2018

@author: rucoma
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import make_classification
from collections import OrderedDict


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
datasetCarsFinal.columns
datasetCarsFinal.head()

# Encoding
le = LabelEncoder()
categorical = datasetCarsFinal.columns[datasetCarsFinal.dtypes == object]
for col in categorical:
    print(col, '#########')
    datasetCarsFinal[col] = le.fit_transform(datasetCarsFinal[col].astype(str))

# Create train and test
np.random.seed(42)
train, test = train_test_split(datasetCarsFinal.index, test_size = 0.2)

X_train = datasetCarsFinal.loc[train].drop(['price'], axis=1)
Y_train = datasetCarsFinal.loc[train]['price']

X_test = datasetCarsFinal.loc[test].drop(['price'], axis=1)
Y_test = datasetCarsFinal.loc[test]['price']

X_train.shape, Y_train.shape 

gsCV_model = RandomForestRegressor(oob_score=True)
params = {
        'n_estimators': [200],
        'max_features':[2,4,8, 'auto'],
        'max_depth':[10,20],
        'min_samples_split':[2,3,4,],
        'min_samples_leaf':[1,2,3]
        }
gsCV = GridSearchCV(gsCV_model,
                    params,
                    n_jobs=-1,
                    verbose=1)

gsCV.fit(X_train, Y_train) # OJO!! Esto tarda un huevo (50 minutos)

print(gsCV.best_score_)
print(gsCV.best_params_)

# Prediccion para test
pred_test = gsCV.predict(X_test)

# Gráfico
plt.plot(Y_test, pred_test, 'o', alpha=0.1)
plt.plot([1, 200000], [1, 200000])

ensemble_clfs = [("RandomForestRegressor, max_depth='20', min_samples_split='3', min_samples_leaf='1'",
                  RandomForestRegressor(warm_start=True, max_features=4, max_depth=20, min_samples_split=3, min_samples_leaf=1, oob_score=True))]
    
error_rate = OrderedDict((label, []) for label, _ in ensemble_clfs)
min_estimators = 30
max_estimators = 1000

for label, clf in ensemble_clfs:
    print(label, clf)
    for i in range(min_estimators, max_estimators + 1, 50):
        clf.set_params(n_estimators=i)
        clf.fit(X_train, Y_train)
        oob_error = 1 - clf.oob_score_
        error_rate[label].append((i, oob_error))
        
error_rate

# Generating "OOB error rate" vs. "n_estimators" plot.
for label, clf_err in error_rate.items():
    xs, ys = zip(*clf_err)
    plt.plot(xs, ys, label=label)
plt.xlim(min_estimators, max_estimators)
plt.xlabel('n_estimarors')
plt.ylabel('OOB error rate')
plt.show()

# fitting set to fine tuned RandomForestRegressor model
y = datasetCarsFinal['price']
X = datasetCarsFinal.drop(['price'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1)
X_train.shape, y_train.shape, X_test.shape, y_test.shape

# Using best params found
model = RandomForestRegressor(max_features=4,
                              max_depth=20,
                              min_samples_leaf=1,
                              oob_score=True,
                              min_samples_split=2,
                              n_estimators=200,
                              n_jobs=-1)

#model = RandomForestRegressor(max_features=4,
#                              max_depth=20,
#                              min_samples_leaf=1,
#                              oob_score=True,
#                              min_samples_split=3,
#                              n_estimators=500,
#                              n_jobs=-1)


model.fit(X_train, y_train)

model.score(X_train, y_train)
model.score(X_test, y_test)

y_pred = model.predict(X_test)

plt.figure(figsize=(6, 4))
plt.scatter(y_test, y_pred, s=20,alpha=0.1)
plt.title('Estimated Price vs. Real Price')
plt.xlabel('Real Price')
plt.ylabel('Predicted Price')

plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'y')
plt.tight_layout()

# feature importance
plt.figure()
plt.title('Feature importance')
plt.bar(range(X.shape[1]), model.feature_importances_, align='center')
plt.xticks(range(X.shape[1]), ('brand', 'model', 'vehicleType', 'gearbox', 'yearOfRegistration',
       'fuelType', 'powerPS', 'kilometerCat', 'notRepairedDamage', 'state'), rotation=90)
plt.show()