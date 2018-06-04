#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 11:38:37 2018

@author: rucoma
2018-06-03
"""
import pandas as pd
pd.set_option("max_columns", 50)
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import tree
from sklearn import neighbors
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import make_classification
from collections import OrderedDict, defaultdict
from sklearn.externals import joblib

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
datasetCarsFinal.columns
datasetCarsFinal.head()
datasetCarsFinal.describe()

# Split dataset into target, numerical and categorical features
target = datasetCarsFinal['price']
numerical = datasetCarsFinal[['yearOfRegistration', 'powerPS']]
categorical = datasetCarsFinal.drop(['yearOfRegistration', 'powerPS', 'price'], axis=1)

# Encoding categorical variables and merging with numerical
d = defaultdict(LabelEncoder)
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
Decission Trees
'''

# parameters
paramGridDT = {
        'criterion': ['mse'],
        'splitter': ['best', 'random'],
        'max_depth': list(range(1, 15 + 1)),
        'min_samples_split': [5],
        'min_samples_leaf': [1],
        'max_features': ['auto']
        }

# Cross Validation (not very long time)
cvDT = GridSearchCV(
        estimator = tree.DecisionTreeRegressor(),
        param_grid=paramGridDT,
        n_jobs=-1,
        cv=10,
        refit=False,
        verbose=1,
        return_train_score=True).fit(X_train, y_train)

# Evaluating the trees
def evaluate_tree(cv):
    if cv.scoring is None:
        scoring = ['score']
    elif type(cv.scoring) == str:
        scoring = [cv.scoring]
    else:
        scoring = cv.scoring

    # cv.cv_results_ contiene un diccionario de arrays; convirtámoslo a DataFrame
    results = pd.DataFrame(cv.cv_results_)
    params = results.params
    results = results.drop('params', axis=1)
    # Dictionary comprenhension
    # Cambiemos el nombre a las columnas que describen los parámetros y pongámoslo en el índice
    param_cols = {
        col: col.replace('param_', '')
        for col in results
        if col.startswith('param_')
    }
    results = results.rename(columns=param_cols).set_index(list(param_cols.values()))
    # Quedémonos sólo con los scores del test final
    results = results[[
        col for col in results
        if any(
            col.endswith('test_' + m) and not col.startswith('split')
            for m in scoring
        )
    ]]

    # Creemos un MultiIndex con esas columnas
    results.columns = pd.MultiIndex.from_tuples([
        [col[0], col[2]]
        for col in map(lambda x: x.split('_'), results.columns)
    ])

    # Definamos un intervalo de confianza al 95% para cada métrica
    low = results['mean'] - 1.96 * results['std']
    high = results['mean'] + 1.96 * results['std']

    for col in low:
        results['low', col] = low[col]
        results['high', col] = high[col]

    # Reordenemos las columnas para analizar mejor cada métrica
    results.columns = pd.MultiIndex.from_tuples([ col[::-1] for col in results ])
    results = results[scoring]

    results.params = params
    if len(scoring) == 1:
        results = results[scoring[0]]

    return(results)
    
evaluation = evaluate_tree(cvDT)
evaluation.head()

# So the best model has this params
evaluation[evaluation['rank'] == 1]

bestDecisionTree = tree.DecisionTreeRegressor(criterion='mse',
                                              max_depth=15,
                                              max_features='auto',
                                              min_samples_leaf=1,
                                              min_samples_split=5,
                                              splitter='best').fit(X_train, y_train)

bestDecisionTree.score(X_train, y_train) #0.9401
bestDecisionTree.score(X_test, y_test)   #0.8599

predTrain = bestDecisionTree.predict(X_train)
predTest = bestDecisionTree.predict(X_test)

MSE = lambda pred, real: np.mean((pred - real) ** 2)
MSE_train = MSE(predTrain, y_train)
MSE_test = MSE(predTest, y_test)


# Charting results
# Train data
plt.figure(figsize=(6, 4))
plt.scatter(y_train, predTrain, s=20,alpha=0.1)
plt.title('Estimated Price vs. Real Price. Train dataset')
plt.xlabel('Real Price')
plt.ylabel('Predicted Price')
plt.plot([min(y_train), max(y_train)], [min(y_train), max(y_train)], 'y')
plt.tight_layout()

# Test data
plt.figure(figsize=(6, 4))
plt.scatter(y_test, predTest, s=20,alpha=0.1)
plt.title('Estimated Price vs. Real Price. Test dataset')
plt.xlabel('Real Price')
plt.ylabel('Predicted Price')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'y')
plt.tight_layout()


# Saving the model
joblib.dump(bestDecisionTree, filename='./output/bestDecisionTree.pkl')

'''
Random Forest
'''
# First try
regrRF = RandomForestRegressor(n_jobs=-1,
                               verbose=1).fit(X_train,
                                              y_train)
regrRF.score(X_train, y_train) #0.9713
regrRF.score(X_test, y_test)   #0.8878

# Params optimization (revisar)
#paramsRF = {
#        'n_estimators': [10, 20, 50, 100],
#        'max_features': [2,4,8, 'auto', None],
#        'max_depth': list(range(3, 10 + 1)),
#        'min_samples_split': [2,3,4],
#        'min_samples_leaf':[1,2,3]
#        }

paramsRF = {
        'n_estimators': [200],
        'max_features': [None],
        'max_depth': list(range(1, 10 + 1)),
        'min_samples_split': [2,3,4],
        'min_samples_leaf':[1,2,3]
        }

# Tarda (más de 5 horas)
cvRF = GridSearchCV(
        estimator=RandomForestRegressor(oob_score=True),
        param_grid=paramsRF,
        n_jobs=-1,
        cv=10,
        verbose=1,
        return_train_score=True).fit(X_train, y_train)

print(cvRF.best_score_) 
print(cvRF.best_params_)

'''
K-nearest Neighbors
'''

#First try
regrKNN = neighbors.KneghborsRegressor(n_neighbors=5, 
                                       weights='distance',
                                       algorithm='auto',
                                       n_jobs=-1).fit(X_train, y_train)
regrKNN.score(X_train, y_train)
regrKNN.score(X_test, y_test)

# Cross Validation
