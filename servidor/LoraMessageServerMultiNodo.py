import time
import config_lora
import pyrebase
import threading
from random import randint

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

*ID emisor: ID del emisor del mensaje, 4 letras

*Saltos: retransmisiones que tuvo el mensaje hasta llegar el receptor, 1 numero

*Datos: datos que se quieren transmitir

-----------------------------------------------------------------------
"""


INTERVAL = 20000         # interval between sends
INTERVAL_BASE = 20000    # interval between sends base




def MessageServer(lora):
    global db
    global IDSERVIDOR
    print("LoRa Server with callback")
    lora.onReceive(on_receive)  # register the receive callback
    db = firebasedb() #inicializa base de datos de Firebase
    
    #busca la id del dispositivos
    try:
        fileID = open("id","rt")
    except FileNotFoundError:
        # doesn't exist
        fileID = open("id","wt")
        IDSERVIDOR = randint(1002,9999)
        fileID.write(str(IDSERVIDOR))
        fileID.close()
    else:
        # exists
        IDSERVIDOR = int(fileID.read())
        fileID.close()
    
    
    print("EL ID del servidor es ", IDSERVIDOR)
    lora.receive()
    do_loop(lora)


def do_loop(lora):    
    
#    lastSendTime = 0
#    interval = 0
    
    while True:
        print("funcionando")
        lora.receive()
        time.sleep(30)
#        now = config_lora.millisecond()
#        if now < lastSendTime: lastSendTime = now 
#        
#        if (now - lastSendTime > interval):
#            lastSendTime = now                                      # timestamp the message
#            interval = (lastSendTime % INTERVAL) + INTERVAL_BASE    # 2-3 seconds
#            print("funcionando")
#            lora.receive()
#            
#            message = "Server online"
#            sendMessage(lora, message)                              # send message
            

#            lora.receive()                                          # go into receive mode
    

def sendMessage(lora, outgoing):
    lora.println(outgoing)
    print("Sending message:\n{}\n".format(outgoing))

    
def on_receive(lora, payload):
    lora.blink_led()   
    
    #send message of receive confirmation
    
    ##############
    
    try:
        payload_string = payload.decode()
        #print("*** Received message ***\n{}".format(payload_string))
        if payload_string[0] != "e":#recive un segundo mensaje con una "e" al inicio
            #Analiza datagrama
            equipo = int(payload_string[0])
            retransmitir = int(payload_string[1])
            idreceptor = int(payload_string[2:6])
            idemisor = int(payload_string[6:10])
            saltos = int(payload_string[10])
            datos = payload_string[11:len(payload_string)]
            
            
            
            if equipo == 1:
                if idreceptor == IDSERVIDOR:#revisa si el mensaje es para el
                    #update date to firebase cloud
                    t = threading.Thread(target=firebaseUpdate, args = (idemisor,datos,)) # uso thred para no pausar el programa hasta que se suban los datos
                    t.daemon = True
                    t.start()   
                    #firebaseUpdate(payload_string)
                    message = str(0)+str(retransmitir)+str(idemisor)+str(IDSERVIDOR)+str(0)+"receive" #emite mensaje de confirmacion de recepcion
                    sendMessage(lora, message)
                    
                elif idreceptor == 1001:
                    message = str(0)+str(retransmitir)+str(idemisor)+str(IDSERVIDOR)+str(0)+"idservidor" #emite mensaje de confirmacion de recepcion
                    sendMessage(lora, message)
            
            #############################################
            
            rssi = lora.packetRssi()
            print("*** Received message ***\n{}".format(payload_string))
            if config_lora.IS_TTGO_LORA_OLED: lora.show_packet(payload_string, rssi)
    except Exception as e:
        print(e)
        
        
    if payload_string[0] != "e":#recive un segundo mensaje con una "e" al inicio
        print("with RSSI {}\n".format(rssi))
    
    lora.receive()           # go into receive mode


def firebasedb():
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
    return db

def firebaseUpdate(idemisor,datos):
    #analizar el string de texto para encontrar las variables a cargar
    
    temperatura = float(datos[0:3])
    humedadSuelo = float(datos[3:6])
    humedadAire = float(datos[6:9])
    
    #####
    
    #listaNodos=db.child("invernaderos/lista").get().val()
    
    #if not idemisor in listaNodos:#busca si el nodo esta en la lista de nodos, si no esta en la lista lo agrega a esta
    #    db.child("invernaderos/lista").update(listaNodos+"|"+idemisor)
    #    db.child("invernaderos/"+idemisor+"contadorultimo").update(0)#crea un dato on la cantidad de datos del invernadero
                
    ###si fija cual es el ultimo lugar de la lista de datos y lo actualiza
    contadorUltimo=db.child("invernaderos/"+idemisor+"contadorultimo").get().val()
    nuevoUltimo=contadorUltimo+1
    db.child("invernaderos/"+idemisor+"contadorultimo").update(nuevoUltimo)
    #########
    
    fecha = time.ctime()[20:24]+time.ctime()[4:7]+time.ctime()[8:10]
    hora =time.ctime()[11:13]+time.ctime()[14:16]
    data = {"temperatura": temperatura, "humedadaire": humedadSuelo, "humedadsuelo": humedadAire, "fecha": fecha+hora}
    db.child("invernaderos/"+str(idemisor)+"/"+str(nuevoUltimo)).update(data)