#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 09:17:53 2018

@author: rucoma
"""

from flask import Flask, render_template, request, flash
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, validators, ValidationError
from django import forms
from sklearn.externals import joblib
import pandas as pd
import numpy as np

#from django.forms import ContactForm

app = Flask(__name__)
app.secret_key = 'development key'

# read csv files
#datasetCarsFinal = pd.read_csv('./data/autosFinal.csv',
#                               usecols=[
#                                      #'brand', 
#                                      #'model', 
#                                      'brandModel',
#                                      'vehicleType', 
#                                      'gearbox', 
#                                      'yearOfRegistration',
#                                      'fuelType',
#                                      'powerPS',
#                                      #'kilometer',
#                                      'kilometerCategorical',
#                                      #'kilometer000',
#                                      'notRepairedDamage',
#                                      #'postalCode',
#                                      'state',
#                                      #'community',
#                                      'price'
#                                      ],
#                               dtype={
#                                      #'brand': 'str', 
#                                      #'model': 'str', 
#                                      'brandModel': 'str', 
#                                      'vehicleType': 'str', 
#                                      'gearbox': 'str', 
#                                      'yearOfRegistration': np.int64,
#                                      'fuelType': 'str',
#                                      'powerPS': np.int64,
#                                      #'kilometer': np.int64,
#                                      'kilometerCategorical': 'str',
#                                      #'kilometer000': np.int64,
#                                      'notRepairedDamage': 'str',
#                                      #'postalCode': 'str',
#                                      'state': 'str',
#                                      #'community':'str',
#                                      'price': np.int64
#                                      })

#class ContactForm(Form):
#    ## Aqui podemos usar una tuple comprenhension como esta:
#    ## [(x, x) for x in sorted(['Hola', 'Yo', 'Tu'])]
#    state = SelectField('Lander', 
#                        choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.state))])
#    brandModel = SelectField('Brand and Model', 
#                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.brandModel))])
#    vehicleType = SelectField('Vehicle Type', 
#                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.vehicleType))])
#    gearbox = SelectField('Gearbox', 
#                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.gearbox))])
#    fuelType = SelectField('Fuel type', 
#                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.fuelType))])
#    powerPS = SelectField('Power PS', 
#                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.powerPS))])
#    kilometerCategorical = SelectField('Kilometers', 
#                             choices = [(x, x) for x in pd.unique(datasetCarsFinal.kilometerCategorical)])
#    yearOfRegistration = SelectField('Year', 
#                             choices = [(x, x) for x in np.arange(datasetCarsFinal.yearOfRegistration.min() + 1, datasetCarsFinal.yearOfRegistration.max())])
#    notRepairedDamage = SelectField('Has the car a damage pending to repair?', 
#                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.notRepairedDamage))])
    
#    name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
#    Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
#    Address = TextAreaField("Address")
#    email = TextField("Email",[validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
#    Age = IntegerField("age")
#    language = SelectField('Languages', choices = [('cpp', 'C++'), ('py', 'Python')])
#    submit = SubmitField("Send data")

@app.route('/', methods = ['GET', 'POST'])

#def hello():
#    rf = joblib.load('./output/102_RandomForestFinal.pkl')
#    return print(rf)

#def results():
#    return print('Hola')

def contact():
   form = ContactForm(request.form) # Este request.form lo he añadido
   
   if request.method == 'POST':
      if form.validate() == True: ## Antes tenia False
         flash('All fields are required.')
         return render_template('form.html', form = form)
      else:
          newdf = pd.DataFrame({'brandModel': request.form['brandModel'],
                          'vehicleType': request.form['vehicleType'],
                          'gearbox': request.form['gearbox'],
                          'yearOfRegistration': request.form['yearOfRegistration'],
                          'fuelType': request.form['fuelType'],
                          'powerPS': request.form['powerPS'],
                          'kilometerCategorical': request.form['kilometerCategorical'],
                          'notRepairedDamage': request.form['notRepairedDamage'],
                          'state': request.form['state']})
#         return render_template('success.html')
          return print(newdf.head())
   elif request.method == 'GET':
         return render_template('form.html', form = form)

if __name__ == "__main__":
#    rf = joblib.load('./output/102_RandomForestFinal.pkl')
#    newdf.head()
    app.run()
    
