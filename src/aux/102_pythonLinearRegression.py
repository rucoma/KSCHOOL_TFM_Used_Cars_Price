#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 19:17:11 2018

@author: rucoma
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
% matplotlib inline
import seaborn as sns
sns.set(style="white")
from subprocess import check_output
#print(check_output(['ls', './data']).decode('utf-8'))
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error

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

## Loop for inspecting categorical variable distributions
#catColumns = ['brand', 'model', 'vehicleType', 'gearbox', 'fuelType']
#for i in catColumns:
#    plt.figure(figsize=(20, 4))
#    plt.title(i + ' Distribution')
#    g = sns.countplot(x = i,
#                      data = datasetCarsFinal,
#                      order=datasetCarsFinal[i].value_counts().index)
#    rotg = g.set_xticklabels(g.get_xticklabels(), rotation=90, size=10)
    
# Another way of doing the same
#for i in catColumns:
#    datasetCarsFinal[i].value_counts().plot(kind='bar', figsize=(18,6))
#    plt.show()

'''
Correlation matrix
'''
corr = datasetCarsFinal[['price', 'yearOfRegistration', 'powerPS', 'kilometer']].corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.2, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

#labels = ['price', 'yearOfRegistration', 'powerPS', 'kilometer']
#fig = plt.figure()
#ax = fig.add_subplot(111)
#cax = plt.matshow(datasetCarsFinal[['price', 'yearOfRegistration', 'powerPS', 'kilometer']].corr())
#fig.colorbar(cax)
#ax.set_xticklabels([''] + labels)
#ax.set_yticklabels([''] + labels)
#plt.show()

'''
Loop for plot relation between year and price by brand
'''

for i in datasetCarsFinal.brand.unique():
    print(i)
    g = sns.pairplot(
        datasetCarsFinal[(datasetCarsFinal.brand == i)],
        x_vars=['yearOfRegistration'],
        y_vars=['price'],
        size=6)
    g.fig.suptitle(i)

'''
Polynomic transformation
'''    
# Creation of train , test datasets
X = datasetCarsFinal[['yearOfRegistration', 'kilometer', 'powerPS']]
y = datasetCarsFinal['price']
poly = PolynomialFeatures(degree=2)
X = poly.fit_transform(X)

# Modelling
np.random.seed(42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

linregr = LinearRegression()
linregr.fit(X_train, y_train)
y_pred_train = linregr.predict(X_train)
y_pred_test = linregr.predict(X_test)

R2_train = r2_score(y_train, y_pred_train) ## Not very good
R2_test = r2_score(y_test, y_pred_test) ## Not very good, but at least no overfitting

# Charting results
plt.figure(figsize=(10, 5))
plt.scatter(y_test, y_pred_test, alpha=.2)
plt.plot([min(y_test), max(y_test)], [min(y_pred_test), max(y_pred_test)])
plt.tight_layout()

'''
No polynomial transformation
'''
# Creation of train , test datasets
X = datasetCarsFinal[['yearOfRegistration', 'kilometer', 'powerPS']]
y = datasetCarsFinal['price']

# Modelling
np.random.seed(42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

linregr = LinearRegression()
linregr.fit(X_train, y_train)
y_pred_train = linregr.predict(X_train)
y_pred_test = linregr.predict(X_test)

R2_train = r2_score(y_train, y_pred_train) ## Not very good
R2_test = r2_score(y_test, y_pred_test) ## Not very good, but at least no overfitting
MSE_train = mean_squared_error(y_train, y_pred_train)
MSE_test = mean_squared_error(y_test, y_pred_test)
RMSE_train = np.sqrt(MSE_train)
RMSE_test = np.sqrt(MSE_test)

# Charting results
plt.figure(figsize=(10, 5))
plt.scatter(y_test, y_pred_test, alpha=.2)
plt.plot([min(y_test), max(y_test)], [min(y_pred_test), max(y_pred_test)])
plt.tight_layout()

## MUCH WORST!!!!

'''
Maybe a model per brand would be better?
'''

def linearRegressionByBrand(brand):
    np.random.seed(42)
    # Creation of train , test datasets
    X = datasetCarsFinal[datasetCarsFinal['brand'] == brand]
    X = X[['yearOfRegistration', 'kilometer', 'powerPS']]
    y = datasetCarsFinal[datasetCarsFinal['brand'] == brand]
    y = y['price']
    poly = PolynomialFeatures(degree=2)
    X = poly.fit_transform(X)
    
    # Modelling
    np.random.seed(42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

    linregr = LinearRegression()
    linregr.fit(X_train, y_train)
    y_pred_train = linregr.predict(X_train)
    y_pred_test = linregr.predict(X_test)

    R2_train = r2_score(y_train, y_pred_train)
    R2_test = r2_score(y_test, y_pred_test)
    return(R2_train, R2_test, X)
    
results = pd.DataFrame({'brand': [], 'score_train': [], 'score_test': []})

for i in datasetCarsFinal.brand.unique():
    print(i)
    score_train, score_test, X = linearRegressionByBrand(i)
    results = results.append({'brand': i, 
                              'score_train': score_train,
                              'score_test': score_test}, 
                              ignore_index=True)
    
'''
Not very sure about that
Maybe would be interesting to use other features
'''