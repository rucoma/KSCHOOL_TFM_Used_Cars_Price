# -*- coding: utf-8 -*-
"""
Created on Fri May  4 18:48:56 2018

@author: Ruben
"""
# http://www.xavierdupre.fr/blog/2015-01-20_nojs.html
import urllib.request

'''
Código para la descarga del dataset de codigos coches en venta
'''

urlDataset = "https://www.dropbox.com/s/3802ph0qspdgtao/autos.csv?dl=1"  # dl=1 is important  https://www.dropbox.com/s/3802ph0qspdgtao/autos.csv?dl=0
u = urllib.request.urlopen(urlDataset)
data = u.read()
u.close()

with open('./data/autos.csv', "wb") as f :
    f.write(data)

'''
Código para la descarga del dataset de codigos postales
'''

urlZipcodes = "https://www.dropbox.com/s/uzzhu05061xjm0z/zipcodes_de_completo.csv?dl=1"
u = urllib.request.urlopen(urlZipcodes)
data = u.read()
u.close()

with open('./data/zipcodes_de_completo.csv', "wb") as f :
    f.write(data)