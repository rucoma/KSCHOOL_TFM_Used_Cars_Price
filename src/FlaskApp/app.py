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

#from django.forms import ContactForm

app = Flask(__name__)
app.secret_key = 'development key'

class ContactForm(Form):
    state = SelectField('Lander', 
                        choices = [('Bayern', 'Bayern'), ('Berlin','Berlin'), ('Barcelona', 'Barcelona'), ('Madrid', 'Madrid')])
    ## Aqui podemos usar una tuple comprenhension como esta:
    ## [(x, x) for x in sorted(['Hola', 'Yo', 'Tu'])]
    brandModel = SelectField('Brand and Model', 
                             choices = [(x, x) for x in sorted(['Hola', 'Yo', 'Tu'])])
    vehicleType = SelectField('Vehicle Type', 
                             choices = [('suv', 'suv'), ('cabrio', 'cabrio'), ('coupe', 'coupe')])
    gearbox = SelectField('Gearbox', 
                             choices = [('automatik', 'automatik'), ('manuell', 'manuell')])
    fuelType = SelectField('Fuel type', 
                             choices = [('diesel', 'diesel'), ('benzin', 'benzin'), ('hybrid', 'hybrid')])
    powerPS = IntegerField("Power PS")
    kilometerCategorical = SelectField('Kilometers', 
                             choices = [('km<50000', 'km<50000'), ('50000>km<100000', '50000>km<100000'), ('km>100000', 'km>100000')])
    yearOfRegistration = IntegerField("Year of registration")
    notRepairedDamage = SelectField('Has the car a damage pending to repair?', 
                             choices = [('ja', 'ja'), ('nein', 'nein')])
    name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
    Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    Address = TextAreaField("Address")
   
    email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
   
    Age = IntegerField("age")
    language = SelectField('Languages', choices = [('cpp', 'C++'), ('py', 'Python')])
    submit = SubmitField("Send")

@app.route('/', methods = ['GET', 'POST'])
def contact():
   form = ContactForm()
   
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('contact.html', form = form)
      else:
         return render_template('success.html')
   elif request.method == 'GET':
         return render_template('contact.html', form = form)

if __name__ == "__main__":
    app.run()
    
