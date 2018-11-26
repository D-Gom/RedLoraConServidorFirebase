# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:13:06 2018

@author: diego
"""

import pyrebase
import datetime
import time
from random import randint

now = datetime.datetime.now()

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
contador=1
while True:
    
    temperatura = randint(0,150)
    humedadSuelo = randint(0,150)
    humedadAire = randint(0,150)
    
    #####
    fechaEspacios = time.ctime()[20:24]+" "+time.ctime()[4:7]+" "+time.ctime()[8:10]+" "
    horaDosPuntos =time.ctime()[11:13]+":"+time.ctime()[14:16]
#    fecha = time.ctime()[20:24]+time.ctime()[4:7]+time.ctime()[8:10]
#    hora =time.ctime()[11:13]+time.ctime()[14:16]
    data = {"temperatura": temperatura, "humedadaire": humedadSuelo, "humedadsuelo": humedadAire, "fecha": fechaEspacios+horaDosPuntos}
#    db.child("invernaderos/"+str(6423)+"/"+fecha+hora).update(data)
    db.child("invernaderos/"+str(5555)+"/"+str(contador)).update(data)
    contador+=1
    
    time.sleep(30)

