import time
import config_lora


INTERVAL = 2000         # interval between sends
INTERVAL_BASE = 2000    # interval between sends base
INTERVAL_BASE_RESEND = 1000 # interval to re send data
msgSendSucces=0
 

def MessageClient(lora):
    print("LoRa Client with callback")
    lora.onReceive(on_receive)  # register the receive callback
    do_loop(lora)


def do_loop(lora):    
    global msgSendSucces
    
    lastSendTime = 0
    interval = 0
    
    while True:
        now = config_lora.millisecond()
        if now < lastSendTime: lastSendTime = now 
        
        if (now - lastSendTime > interval):
            lastSendTime = now                                      # timestamp the message
            interval = (lastSendTime % INTERVAL) + INTERVAL_BASE    # 2-3 seconds
            
            #message = "{} {}".format(config_lora.NODE_NAME, msgCount)
            message = "temperatura: 20;HumedadSuelo: 70;HumedadAire: 50"
            sendMessage(lora, message)                              # send message
            

            lora.receive()                                          # go into receive mode
		
		
        if (now - lastSendTime > INTERVAL_BASE_RESEND) and msgSendSucces==1 :            
            #message = "{} {}".format(config_lora.NODE_NAME, msgCount)
            message = "temperatura: 20;HumedadSuelo: 70;HumedadAire: 50"
            sendMessage(lora, message)                              # send message
            

            lora.receive()                                          # go into receive mode
		
    

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