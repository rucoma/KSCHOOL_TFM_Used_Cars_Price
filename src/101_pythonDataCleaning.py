#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 22:27:12 2018

@author: rucoma
"""

# Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Read data
datasetCars = pd.read_csv('./data/autos.csv', 
                          encoding='latin-1',
                          #dtype={'a': np.float64, 'b': 'str', 'c': np.int64},
                          dtype={'dateCrawled': 'str', 
                                 'name': 'str',
                                 'seller': 'str',
                                 'offerType': 'str',
                                 'price': np.int64,
                                 'abtest': 'str',
                                 'vehicleType': 'str',
                                 'yearOfRegistration': np.int64,
                                 'gearbox': 'str',
                                 'powerPS': np.int64,
                                 'model': 'str',
                                 'kilometer': np.int64,
                                 'monthOfRegistration': np.int64,
                                 'fuelType': 'str',
                                 'brand': 'str',
                                 'notRepairedDamage': 'str',
                                 'dateCreated': 'str',
                                 'nrOfPictures': np.int64,
                                 'postalCode': 'str',
                                 'lastSeen': 'str'})

columnsOriginal = datasetCars.columns

# Select features
datasetCarsMinimal = datasetCars[['seller', 'offerType', 'price', 'vehicleType', 
                                  'yearOfRegistration', 'gearbox', 'powerPS', 
                                  'model', 'kilometer', 'fuelType', 'brand', 
                                  'notRepairedDamage', 'postalCode']]
# Review values for each feature
print('########## Categorical variables ###########')
for i in datasetCarsMinimal.columns:
    if datasetCarsMinimal[i].dtypes == 'object':
        print('FEATURE: ', i, '######')
        print(datasetCarsMinimal[i].value_counts())

print('########## Numerical variables ##########')        
for i in datasetCarsMinimal.columns:
    if datasetCarsMinimal[i].dtypes != 'object':
        print('FEATURE: ', i, '######')
        print(datasetCarsMinimal[i].unique())
        
# Remove undesired values
datasetCarsMinimal = datasetCarsMinimal[datasetCarsMinimal.seller == 'privat']
datasetCarsMinimal = datasetCarsMinimal[datasetCarsMinimal.offerType == 'Angebot']
datasetCarsMinimal = datasetCarsMinimal[datasetCarsMinimal.brand != 'sonstige_autos']

# Inspecting model feature
datasetCarsMinimal['model'] = datasetCarsMinimal.model.astype(str)
datasetCarsMinimal = datasetCarsMinimal[datasetCarsMinimal.seller != 'nan']

models = datasetCarsMinimal['model'].unique()
models = sorted(models)
len(models)
# Nothing to clean here

# Remove NA values
# Some inspection first
for i in datasetCarsMinimal.columns:
    print('FEATURE: ', i)
    print(datasetCarsMinimal[i].isnull().sum())
    
datasetCarsMinimalNoNA = datasetCarsMinimal.dropna()
datasetCarsMinimalNoNA.shape

## Visual inspection of the numeric features
# Price
plt.hist(datasetCarsMinimalNoNA['price'], bins=100)
# Something strange here...
max(datasetCarsMinimalNoNA.price)
min(datasetCarsMinimalNoNA.price)
plt.hist(datasetCarsMinimalNoNA.price[datasetCarsMinimalNoNA['price'] < 200000], 
         bins=50)
# Filtering prices below 200K€
datasetCarsMinimalNoNA = datasetCarsMinimalNoNA[(datasetCarsMinimalNoNA['price'] <= 200000) & 
                                                (datasetCarsMinimalNoNA['price'] > 200)]
plt.hist(datasetCarsMinimalNoNA['price'], bins=100)
datasetCarsMinimalNoNA.shape

# Year
plt.hist(datasetCarsMinimalNoNA['yearOfRegistration'], bins=75)
max(datasetCarsMinimalNoNA.yearOfRegistration)
min(datasetCarsMinimalNoNA.yearOfRegistration)

# PowerPS
plt.hist(datasetCarsMinimalNoNA['powerPS'], bins=100)
max(datasetCarsMinimalNoNA.powerPS)
min(datasetCarsMinimalNoNA.powerPS)
# Cleaning powerPS
datasetCarsMinimalNoNA = datasetCarsMinimalNoNA[(datasetCarsMinimalNoNA.powerPS > 0) & (datasetCarsMinimalNoNA.powerPS <= 1000)]
plt.hist(datasetCarsMinimalNoNA['powerPS'], bins=100)
plt.hist(np.log(datasetCarsMinimalNoNA['powerPS']), bins=100)
#datasetCarsMinimalNoNA['logPowerPS'] = np.log(datasetCarsMinimalNoNA['powerPS'])
#datasetCarsMinimalNoNA = datasetCarsMinimalNoNA.drop(['powerPS'], axis=1)
#datasetCarsMinimalNoNA.columns

# Kilometer
plt.hist(datasetCarsMinimalNoNA['kilometer'], bins=50)
datasetCarsMinimalNoNA['kilometerCat'] = pd.cut(datasetCarsMinimalNoNA['kilometer'], 
                      [0, 50000, 100000, 150000, math.inf], 
                      labels=['km<=50000', '50000>km<=100000', '100000>km<=150000', 'km>150000'])
datasetCarsMinimalNoNA['kilometer000'] = datasetCarsMinimalNoNA['kilometer'] / 1e3

# Copy the dataset
datasetCarsFinal = datasetCarsMinimalNoNA.copy()
# Drop unused variables
datasetCarsFinal = datasetCarsFinal.drop(['seller', 'offerType'], axis=1)
datasetCarsFinal.head()
arrangedCols = ['brand', 'model', 'vehicleType', 'gearbox', 'yearOfRegistration', 
                'fuelType', 'powerPS', 'kilometer', 'kilometerCat', 'kilometer000', 
                'notRepairedDamage', 'postalCode', 'price']
datasetCarsFinal = datasetCarsFinal[arrangedCols]



fileZipcodes = '~/Dropbox/MOOCs/KSCHOOL/DATA SCIENCE/TFM/zipcodes_de_completo.csv'
zipcodes = pd.read_csv(fileZipcodes, 
                  encoding='UTF-8',
                  usecols=[
                          #'country_code', 
                           'zipcode', 
                           #'place', 
                           'state', 
                           #'state_code', 
                           #'province',
                           #'province_code', 
                           #'community',
                           #'community_code', 
                           #'latitude',
                           #'longitude'
                           ],
                  dtype= {
                          #'country_code': 'str', 
                           'zipcode': 'str', 
                           #'place': 'str', 
                           'state': 'str', 
                           #'state_code': 'str', 
                           #'province': 'str',
                           #'province_code': 'str', 
                           #'community': 'str',
                           #'community_code': 'str', 
                           #'latitude': np.float64,
                           #'longitude': np.float64
                           })

zipcodes.drop_duplicates(subset='zipcode', 
                         keep='first', 
                         inplace=True)

datasetCarsFinal = datasetCarsFinal.merge(zipcodes,
                                          left_on='postalCode', 
                                          right_on='zipcode', 
                                          how='left')

### OJO, VAMOS A SELECCIONAR SOLO ALGUNAS PARA MODELIZAR
finalCols = ['brand', 
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
             'price']

datasetCarsFinal = datasetCarsFinal[finalCols]

# Save dataset in a new csv file
datasetCarsFinal.to_csv('./data/autosFinal.csv',
                        header=True,
                        index=False)

# Remove unused datasets and variables
del(datasetCarsMinimal)
del(datasetCarsMinimalNoNA)
del(datasetCars)
del(i)
del(models)
del(arrangedCols)
del(finalCols)
del(zipcodes)
del(fileZipcodes)

'''
FINISH!!
LET'S GO TO MODELLING
'''