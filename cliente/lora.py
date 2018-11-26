# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:46:57 2018

@author: diego
"""
import sx127x
import config_lora 





class lora:
    
    def __init__(self):
        
        self.controller = config_lora.Controller()

        self.lora = self.controller.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                      pin_id_ss = config_lora.Controller.PIN_ID_FOR_LORA_SS,
                                      pin_id_RxDone = config_lora.Controller.PIN_ID_FOR_LORA_DIO0)
    
        
        self.INTERVAL_BASE_RESEND = 10000 # interval to re send data
        
        self.msgSendFlag=0
        
        self.MessageClient()
     

    def MessageClient(self):
        print("LoRa Client with callback")
        self.lora.onReceive(self.on_receive)  # register the receive callback
    
    
    def sendMeasurements(self, temp, humS, humA): 
        
        """       
        -----------------------------------------------------------------------
        Datagrama mensaje
        
        -------------------------------------------------------------------------------
        |Servidor(0)/Nodo(1)||Restransmitir||ID receptor||ID emisor||Saltos||  Datos ||
        -------------------------------------------------------------------------------
        
        *Servidor/Nodo: 0 - El mesaje fue emitido por un servidor
                        1 - El mensaje fue emitido por un nodo
        
        *Restransmitir: 0 - Los nodos no retransmiten el mensaje
                        1 - Los nodos retransmiten el mensaje
        
        *ID receptor:ID del receptor del mensaje
        
        *ID emisor: ID del emisor del mensaje
        
        *Saltos: retransmisiones que tuvo el mensaje hasta llegar el receptor
        
        Datos: datos que se quieren transmitir
        
        -----------------------------------------------------------------------
        """        
        
        firstTime = 0
        lastSendTime = 0
#        message = "{} {}".format(config_lora.NODE_NAME, msgCount)
    
        self.lora.receive()
        
        while True:
            now = config_lora.millisecond()
            if now < lastSendTime: lastSendTime = now 
            
            if firstTime==0:                                
                message = "temperatura: "+str(temp)+";HumedadSuelo: "+str(humS)+";HumedadAire: "+str(humA)
                self.sendMessage(self.lora, message)                              # send message
                self.msgSendFlag=1
                firstTime=1
            		
            if (now - lastSendTime > self.INTERVAL_BASE_RESEND) and self.msgSendFlag==1 :          
                lastSendTime = now                                      # timestamp the message
                #message = "{} {}".format(config_lora.NODE_NAME, msgCount)
                #message = "temperatura: 20;HumedadSuelo: 70;HumedadAire: 50"
                message = "temperatura: "+str(temp)+";HumedadSuelo: "+str(humS)+";HumedadAire: "+str(humA)
                self.sendMessage(self.lora, message)                              # send message
                
    
            self.lora.receive()                                          # go into receive mode
                
            if self.msgSendFlag == 0:
                break
                
    
    def sendMessage(self,lora, outgoing):
        self.lora.println(outgoing)
        print("Sending message:\n{}\n".format(outgoing))
    
        
    def on_receive(self,lora, payload):
        
        self.lora.blink_led()   
        
        try:
            payload_string = payload.decode()
            rssi = self.lora.packetRssi()
            print("*** Received message ***\n{}".format(payload_string))
            if config_lora.IS_TTGO_LORA_OLED: lora.show_packet(payload_string, rssi)
        except Exception as e:
            print(e)
        print("with RSSI {}\n".format(rssi))
        
    	#Check receive confirmation 
        if (payload_string=="receive"):
            self.msgSendFlag=1
    
    