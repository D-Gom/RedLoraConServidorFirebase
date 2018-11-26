# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 15:46:57 2018

@author: diego
"""


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

*ID receptor:ID del receptor del mensaje, 4 letras

*ID emisor: ID del emisor del mensaje, 4 numeros

*Saltos: retransmisiones que tuvo el mensaje hasta llegar el receptor, 1 numero

*Datos: datos que se quieren transmitir

-----------------------------------------------------------------------
"""  
        
        
import sx127x
import config_lora 

from random import randint


class lora:
    
    def __init__(self):
        
        self.controller = config_lora.Controller()

        self.lora = self.controller.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                      pin_id_ss = config_lora.Controller.PIN_ID_FOR_LORA_SS,
                                      pin_id_RxDone = config_lora.Controller.PIN_ID_FOR_LORA_DIO0)
    
        
        self.INTERVAL_BASE_RESEND = 10000 # interval to resend data
        
        self.msgSendFlag = 0
        self.IDSERVIDOR = 1001# el id 1001 es cuando no sabe quien es el servidor
        self.IDNODO = 0000
        #busca la id del dispositivos
        try:
            fileID = open("id","rt")
        except FileNotFoundError:
            # doesn't exist
            fileID = open("id","wt")
            self.IDSNODO = randint(1002,9999)
            fileID.write(str(self.IDSNODO))
            fileID.close()
        else:
            # exists
            self.IDNODO = int(fileID.read())
            fileID.close()
            
            
        print("EL ID del nodo es ", self.IDNODO)
        self.MessageClient()
     

    def MessageClient(self):
        print("LoRa Client with callback")
        
        self.lora.onReceive(self.on_receive)  # register the receive callback
        
        message = str(1)+str(1)+str(1001)+str(self.IDNODO)+str(0)+"buscando servidor" #emite mensaje de confirmacion de recepcion
        self.sendMessage(self.lora, message)                              # send message
        self.lora.receive()
    
    def sendMeasurements(self, temp, humS, humA): 
        
              
        
        firstTime = 0
        lastSendTime = 0
        datos = "{}{}{}".format(*str(float(temp)))+"{}{}{}".format(*str(float(humS)))+"{}{}{}".format(*str(float(humA)))
        
        
        if self.IDSERVIDOR == 1001:
            message = str(1)+str(1)+str(1001)+str(self.IDNODO)+str(0)+"buscando servidor" #emite mensaje de confirmacion de recepcion
            self.sendMessage(self.lora, message)                              # send message
            self.lora.receive()
       
        else:         
        
            while True:
                now = config_lora.millisecond()
                if now < lastSendTime: lastSendTime = now 
                
                if firstTime == 0:          
                    lastSendTime = now                          
                    message = str(1)+str(0)+str(self.IDSERVIDOR)+str(self.IDNODO)+str(0)+datos#envia los datos al servidor
                    self.sendMessage(self.lora, message)                              # send message
                    self.msgSendFlag=1
                    firstTime=1
                		
                elif (now - lastSendTime > self.INTERVAL_BASE_RESEND) and self.msgSendFlag==1 :          
                    lastSendTime = now                                      # timestamp the message
                    message = str(1)+str(1)+str(self.IDSERVIDOR)+str(self.IDNODO)+str(0)+datos#envia los datos al servidor haciendo uso de los otros nodos
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
            
            #Analiza datagrama
            equipo = int(payload_string[0])
            retransmitir = int(payload_string[1])
            idreceptor = int(payload_string[2:6])
            idemisor = int(payload_string[6:10])
            saltos = int(payload_string[10])
            datos = payload_string[11:len(payload_string)]
            
            if equipo == 0:
                if idreceptor == self.IDNODO:
                    if (datos == "receive"):#revisa si es confirmacion de recepcion
                        self.msgSendFlag = 0
                    elif (datos == "idservidor"):#recive la id del servidor
                        self.IDSERVIDOR = idemisor
                else:
                    if retransmitir == 1:#revisa si tiene que retransmitir
                        if saltos < 9:#si ya se retransmitio mas de 9 veces no se retransmite mas
                            message = str(equipo)+str(retransmitir)+str(idreceptor)+str(idemisor)+str(saltos+1)+datos #retransmite el mensaje sumando 1 a los saltos
                            self.sendMessage(self.lora, message)
                
            if equipo == 1:#revisa si es un nodo el que transmite
                if retransmitir == 1:#revisa si tiene que retransmitir
                    if idemisor != self.IDNODO:#revisa que no sea su propio mensaje                           
                        if saltos < 9:#si ya se retransmitio mas de 10 veces no se retransmite mas
                            message=str(equipo)+str(retransmitir)+str(idreceptor)+str(idemisor)+str(saltos+1)+datos #retransmite el mensaje sumando 1 a los saltos
                            self.sendMessage(self.lora, message)
            
                
            
            rssi = self.lora.packetRssi()
            print("*** Received message ***\n{}".format(payload_string))
            if config_lora.IS_TTGO_LORA_OLED: lora.show_packet(payload_string, rssi)
        except Exception as e:
            print(e)
        print("with RSSI {}\n".format(rssi))
        
    
    