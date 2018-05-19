#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 12:48:41 2018

@author: rucoma
"""

import pandas as pd
import numpy as np



''' Estos no sirven

file1 = '~/Dropbox/MOOCs/KSCHOOL/DATA SCIENCE/TFM/de_postal_codes.csv'
df1 = pd.read_csv(file1, 
                  encoding='ISO-8859-15',
                  usecols=['Postal Code',
                           'Place Name',
                           'State',
                           'State Abbreviation',
                           'City',
                           'Latitude',
                           'Longitude'],
                  dtype={'Postal Code': 'str',
                         'Place Name': 'str',
                         'State': 'str',
                         'State Abbreviation':'str',
                         'City': 'str',
                         'Latitude': np.float64,
                         'Longitude': np.float64})
# Este no es muy bueno
file2 = '~/Dropbox/MOOCs/KSCHOOL/DATA SCIENCE/TFM/German-Zip-Codes.csv'
df2 = pd.read_csv(file2, 
                  encoding='UTF-8', 
                  sep=';',
                  usecols=['Ort',
                           'Zusatz',
                           'Plz',
                           'Vorwahl',
                           'Bundesland'],
                  dtype={'Ort': 'str',
                           'Zusatz': 'str',
                           'Plz': 'str',
                           'Vorwahl': 'str',
                           'Bundesland': 'str'})

'''

file3 = '~/Dropbox/MOOCs/KSCHOOL/DATA SCIENCE/TFM/zipcodes_de_completo.csv'
df3 = pd.read_csv(file3, 
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

df3.drop_duplicates(subset='zipcode', keep='first', inplace=True)

#xx = df3.groupby('zipcode').count()
#duplicated_zip = xx.index[xx.state == 2]
#df3[df3.zipcode.isin(duplicated_zip)].sort_values(by='zipcode')

dataset = datasetCarsFinal.merge(df3, left_on='postalCode', right_on='zipcode', how='left')
