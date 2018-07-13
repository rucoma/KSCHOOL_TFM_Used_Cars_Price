#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 18:42:21 2018

@author: rucoma
Resources:
https://www.tutorialspoint.com/flask/flask_wtf.htm
https://ampersandacademy.com/tutorials/flask-framework/flask-framework-form-values

"""
from flask import Flask, render_template, request, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField, SubmitField
import pandas as pd
import numpy as np
from sklearn.externals import joblib

app = Flask(__name__)
app.secret_key = 'development key'


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

bestBoost = joblib.load('./output/bestBoost.pkl')
le = joblib.load('./output/carsLabelEncoder.pkl')

class DataForm(Form):
    state = SelectField('Which is your Lander?',
                        choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.state))])
    brandModel = SelectField('Brand and Model of the car',
                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.brandModel))])
    vehicleType = SelectField('Vehicle Type',
                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.vehicleType))])
    gearbox = SelectField('Gearbox',
                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.gearbox))])
    fuelType = SelectField('Fuel type',
                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.fuelType))])
    powerPS = SelectField('Power PS',
                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.powerPS))])
    kilometer = SelectField('Kilometers',
                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.kilometer))])
    yearOfRegistration = SelectField('Year of registration',
                             choices = [(x, x) for x in np.arange(datasetCarsFinal.yearOfRegistration.min() + 1, datasetCarsFinal.yearOfRegistration.max())])
    notRepairedDamage = SelectField('Has the car a damage pending to repair?',
                             choices = [(x, x) for x in sorted(pd.unique(datasetCarsFinal.notRepairedDamage))])
    submit = SubmitField("Send data")

@app.route('/', methods=['GET', 'POST'])
def contact():
   form = DataForm()


#    Codigo Original
   if request.method == 'POST':
      if form.validate() == True:
         flash('All fields are required.')
         return render_template('form.html', form = form)
      else:
#         state = form.get('state')
#         kilometer = form.get('kilometer')
         state = request.form['state']
         brandModel = request.form['brandModel']
         vehicleType = request.form['vehicleType']
         gearbox = request.form['gearbox']
         fuelType = request.form['fuelType']
         powerPS = request.form['powerPS']
         kilometer = request.form['kilometer']
         yearOfRegistration = request.form['yearOfRegistration']
         notRepairedDamage = request.form['notRepairedDamage']

         '''
         Aqui meter el codigo para label encoder y predict
         '''

         return render_template('success.html',
                                state=state,
                                brandModel=brandModel,
                                vehicleType=vehicleType,
                                gearbox=gearbox,
                                fuelType=fuelType,
                                powerPS=powerPS,
                                kilometer=kilometer,
                                yearOfRegistration=yearOfRegistration,
                                notRepairedDamage=notRepairedDamage)
   elif request.method == 'GET':
         return render_template('form.html', form = form)

   '''
   Nuevo codigo
   if request.method == 'POST':
       if form.validate == False:
           return render_template('success.html')
       else:
           return render_template('form.html', form = form)
   '''

@app.route('/another', methods=['GET', 'POST'])
def hello():
    form = DataForm()

    if request.method == 'POST':
        return render_template('form.html', form = form)


if __name__ == '__main__':
    app.run(debug = True)
