# -*- coding: utf-8 -*-
"""
Random Forest with python
2018-04-29

Este script nos da un resultado de 0.9 en train y 0.83 en test
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn import tree
import graphviz

# Read CSV final
datasetCarsFinal = pd.read_csv('./data/autosFinal.csv')
print(datasetCarsFinal.shape)
print(datasetCarsFinal.head())

# Create train and test indexes
np.random.seed(42)
train, test = train_test_split(datasetCarsFinal.index, test_size = 0.2)

'''
Decission trees
'''

# Creation of features matrix and dummy variables
features = datasetCarsFinal.drop('price', axis = 1)
features = pd.get_dummies(features)
features.head()
features.shape

regr = tree.DecisionTreeRegressor().fit(features.loc[train], datasetCarsFinal.price[train])

regr.feature_importances_


treeData = tree.export_graphviz(regr, out_file=None)
graph = graphviz.Source(treeData)

# No ejecutar
# graph

regr.score(features.loc[train], datasetCarsFinal.price[train])
regr.score(features.loc[test], datasetCarsFinal.price[test])

# Predictions
pred = pd.Series(regr.predict(features), index = datasetCarsFinal.index)

plt.scatter(datasetCarsFinal.price.loc[train], pred.loc[train], color='gray', alpha=.1)
plt.scatter(datasetCarsFinal.price.loc[test], pred.loc[test], color='blue', alpha=.1)

# Parameters
paramGrid = {
        'max_depth': list(range(1, 12 + 1)),
        'splitter': ['best', 'random']}

# Tarda un poco
cv = GridSearchCV(
        tree.DecisionTreeRegressor(),
        param_grid = paramGrid,
        n_jobs=-1,
        cv=5,
        refit=False).fit(features.loc[train], datasetCarsFinal.price[train])

def evaluate_tree(cv):
    if cv.scoring is None:
        scoring = ['score']
    elif type(cv.scoring) == str:
        scoring = [cv.scoring]
    else:
        scoring = cv.scoring

    # cv.cv_results_ contiene un diccionario de arrays; convirtámoslo a DataFrame
    results = pd.DataFrame(cv.cv_results_)

    # Quedémonos con params, que tiene cada configuración de parámetros
    params = results.params
    results = results.drop('params', axis=1)

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

    return results

results = evaluate_tree(cv)
results

# Con los resultados obtenidos podemos establecer que la mejor combinacion de
# parametros es max_depth = 12 y splitter = best

regrBest = tree.DecisionTreeRegressor(
        max_depth = 12,
        splitter = 'best').fit(features.loc[train], datasetCarsFinal.price[train])

regrBest.score(features.loc[train], datasetCarsFinal.price[train]), regrBest.score(features.loc[test], datasetCarsFinal.price[test])

predBest = pd.Series(regrBest.predict(features), index=datasetCarsFinal.index)
predBest
'''
# Hyperparameters optimization
hyp = {
       'criterion': ['gini', 'entropy'],
       'max_depth': [4, 5, 6, 7, 8, 9, 10, 11, 12],
       'min_samples_split': [2, 4, 6, 8, 10],
       'min_samples_leaf': [1, 5, 10],
       'min_weight_fraction_leaf': [.1, .2, .3],
       'max_leaf_nodes': [64, 128, 256],
       'splitter': ['best', 'random']
       }

from functools import reduce
reduce(lambda x, y: x * len(y), hyp.values(), 1) / 60 / 24
'''
