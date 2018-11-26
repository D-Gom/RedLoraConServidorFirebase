import time
import config_lora
import pyrebase
import datetime
import threading

#now = datetime.datetime.now()



msgCount = 0            # count of outgoing messages
INTERVAL = 20000         # interval between sends
INTERVAL_BASE = 20000    # interval between sends base



def MessageServer(lora):
    global db
    print("LoRa Server with callback")
    lora.onReceive(on_receive)  # register the receive callback
    db = firebasedb()
    do_loop(lora)


def do_loop(lora):    
    global msgCount
    
    lastSendTime = 0
    interval = 0
    
    while True:
        now = config_lora.millisecond()
        if now < lastSendTime: lastSendTime = now 
        
        if (now - lastSendTime > interval):
            lastSendTime = now                                      # timestamp the message
            interval = (lastSendTime % INTERVAL) + INTERVAL_BASE    # 2-3 seconds
            
            message = "Server online"
            sendMessage(lora, message)                              # send message
            msgCount += 1 

            lora.receive()                                          # go into receive mode
    

def sendMessage(lora, outgoing):
    lora.println(outgoing)
    print("Sending message:\n{}\n".format(outgoing))

    
def on_receive(lora, payload):
    lora.blink_led()   
    
    #send message of receive confirmation
    
    message = "receive" #send parameters to cloud
    sendMessage(lora, message)  
    lora.receive()           # go into receive mode
    ##############
    
    try:
        payload_string = payload.decode()
        t = threading.Thread(target=firebaseUpdate, args = (payload_string,))
        t.daemon = True
        t.start()   
        #firebaseUpdate(payload_string)
        
        rssi = lora.packetRssi()
        print("*** Received message ***\n{}".format(payload_string))
        if config_lora.IS_TTGO_LORA_OLED: lora.show_packet(payload_string, rssi)
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(rssi))


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

def firebaseUpdate(msg):
    #analizar el string de texto para encontrar las variables a cargar
    
    temperatura = msg[13:15]
    humedadSuelo = msg[30:32]
    humedadAire = msg[46:48]
    
    #####
    data = {"temperatura": temperatura, "humedadaire": humedadSuelo, "humedadsuelo": humedadAire}
    
    db.child(str(datetime.datetime.now().minute)).update(data)