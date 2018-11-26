# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 12:56:53 2018

@author: diego
"""

import time
import config_lora


INTERVAL = 2000         # interval between sends
INTERVAL_BASE = 2000    # interval between sends base
INTERVAL_BASE_RESEND = 1000 # interval to re send data
msgSendSucces=0
 

def MessageClient(lora):
    print("LoRa Client with callback")
    lora.onReceive(on_receive)  # register the receive callback


def sendMeasurements(lora, temp, humS, humA):    
    global msgSendSucces
    
    lastSendTime = 0
    #message = "{} {}".format(config_lora.NODE_NAME, msgCount)

    lora.receive()
    
    while True:
        now = config_lora.millisecond()
        if now < lastSendTime: lastSendTime = now 
        		
        if (now - lastSendTime > INTERVAL_BASE_RESEND) and msgSendSucces==1 :          
            lastSendTime = now                                      # timestamp the message
            #message = "{} {}".format(config_lora.NODE_NAME, msgCount)
            #message = "temperatura: 20;HumedadSuelo: 70;HumedadAire: 50"
            message = "temperatura: "+temp+";HumedadSuelo: "+humS+";HumedadAire: "+humA
            sendMessage(lora, message)                              # send message
            

            lora.receive()                                          # go into receive mode
            
        elif msgSendSucces == 0:
            break
            

def sendMessage(lora, outgoing):
    lora.println(outgoing)
    print("Sending message:\n{}\n".format(outgoing))

    
def on_receive(lora, payload):
    global msgSendSucces
    lora.blink_led()   
    
    try:
        payload_string = payload.decode()
        rssi = lora.packetRssi()
        print("*** Received message ***\n{}".format(payload_string))
        if config_lora.IS_TTGO_LORA_OLED: lora.show_packet(payload_string, rssi)
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(rssi))
    
	#Check receive confirmation 
    if (payload_string=="receive"):
        msgSendSucces=1