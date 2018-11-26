# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 13:18:44 2018

@author: diego
"""
#install:
#       pip rpi-gpio
#
#Enable SPI in rasp-config

import lora
import config_lora
from random import randint


INTERVAL = 100000         # interval between sends
temp = 20
humS = 20
humA = 20





def main():
    transceiver= lora.lora()
    lastSendTime = 0
    while True:
        now = config_lora.millisecond()
        
        if now < lastSendTime: lastSendTime = now 
        
        if (now - lastSendTime > INTERVAL):
            lastSendTime = now
            #transceiver.sendMeasurements(temp, humS, humA)
            transceiver.sendMeasurements(randint(1,99),
                                         randint(1,99),
                                         randint(1,99))
            
            print("Sendiang message")
                     
            
if __name__ == '__main__':
    main()