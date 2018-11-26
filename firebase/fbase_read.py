# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:03:13 2018

@author: diego
"""

import pyrebase

config = {
    "apiKey": "AIzaSyBhjWF2cO0l3XSp_CaGLONozaUwu8tP1IY",
    "authDomain": "iotutepsa-5765c.firebaseapp.com",
    "databaseURL": "https://iotutepsa-5765c.firebaseio.com",
    "projectId": "iotutepsa-5765c",
    "storageBucket": "iotutepsa-5765c.appspot.com",
    "messagingSenderId": "644877536033"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

salida_logico=db.child("database/logico").get()
salida_numerico=db.child("database/numerico").get()
salida_texto=db.child("database/texto").get()

print("salida logico: ",salida_logico.val())
print("salida numerico: ", salida_numerico.val())
print("salida texto: ", salida_texto.val())
