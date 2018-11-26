# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 13:18:44 2018

@author: diego
"""
#install:
#       pip rpi-gpio
#
#Enable SPI in rasp-config

import loraMultiNodo
import config_lora
import time
from random import randint


INTERVAL = 50000         # interval between sends
temp = 20
humS = 20
humA = 20





def main():
    transceiver= loraMultiNodo.lora()
#    lastSendTime = 0
    while True:
        transceiver.sendMeasurements(randint(0,150),
                                     randint(0,100),
                                     randint(0,100))
        time.sleep(20)
#        now = config_lora.millisecond()
#        
#        if now < lastSendTime: lastSendTime = now 
#        
#        if (now - lastSendTime > INTERVAL):
#            lastSendTime = now
#            #transceiver.sendMeasurements(temp, humS, humA)
#            transceiver.sendMeasurements(randint(11,99),
#                                         randint(11,99),
#                                         randint(11,99))
#            
#            print("Sendiang message")
                     
            
if __name__ == '__main__':
    main()