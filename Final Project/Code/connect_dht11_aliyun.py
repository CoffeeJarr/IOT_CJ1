# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import hashlib
import hmac
import random
import json
import RPi.GPIO as GPIO
import numpy as np
import time
# This is the triplet when we register our products and devices in Aliyun
# just fill in our own triples
options = {
    'productKey':'###',
    'deviceName':'###',
    'deviceSecret':'###',
    'regionId':'cn-shanghai'
}

DHTPIN = 4         

GPIO.setmode(GPIO.BCM)      

def read_dht11_dat():
    
    GPIO.setup(DHTPIN, GPIO.OUT)
    GPIO.output(DHTPIN, GPIO.LOW)
    time.sleep(0.02)                
    GPIO.output(DHTPIN, GPIO.HIGH)  
    GPIO.setup(DHTPIN, GPIO.IN)    
    while GPIO.input(DHTPIN) == GPIO.LOW:
        continue
    while GPIO.input(DHTPIN) == GPIO.HIGH:
        continue
# receive the data
    j = 0            
    data = []         
    kk=[]            
    while j < 40:
        k = 0
        while GPIO.input(DHTPIN) == GPIO.LOW:  
            continue
        while GPIO.input(DHTPIN) == GPIO.HIGH:
            k += 1
            if k > 100:
                break
        kk.append(k)
        if k < 20:      
            data.append(0)      
        else:          
            data.append(1)      
 
        j += 1
 
    print("sensor is working.")
    print('初始数据高低电平:\n',data)   
    print('参数k的列表内容：\n',kk)    
    m = np.logspace(7,0,8,base=2,dtype=int) 
    data_array = np.array(data) 
    humidity = m.dot(data_array[0:8])       
    humidity_point = m.dot(data_array[8:16])
    temperature = m.dot(data_array[16:24])
    temperature_point = m.dot(data_array[24:32])
    check = m.dot(data_array[32:40])
    print(humidity,humidity_point,temperature,temperature_point,check)
    tmp = humidity + humidity_point + temperature + temperature_point
    return humidity, temperature


HOST = options['productKey'] + '.iot-as-mqtt.'+options['regionId']+'.aliyuncs.com'
PORT = 1883 
PUB_TOPIC = "/sys/" + options['productKey'] + "/" + options['deviceName'] + "/thing/event/property/post";


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("the/topic")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def hmacsha1(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha1).hexdigest()

def getAliyunIoTClient():
    timestamp = str(int(time.time()))
    CLIENT_ID = "paho.py|securemode=3,signmethod=hmacsha1,timestamp="+timestamp+"|"
    CONTENT_STR_FORMAT = "clientIdpaho.pydeviceName"+options['deviceName']+"productKey"+options['productKey']+"timestamp"+timestamp
    # set username/password.
    USER_NAME = options['deviceName']+"&"+options['productKey']
    PWD = hmacsha1(options['deviceSecret'],CONTENT_STR_FORMAT)
    client = mqtt.Client(client_id=CLIENT_ID, clean_session=False)
    client.username_pw_set(USER_NAME, PWD)
    return client


if __name__ == '__main__':
    while True:
        try:
            client = getAliyunIoTClient()
            client.on_connect = on_connect
            client.on_message = on_message
            
            client.connect(HOST, 1883, 300)

            print("Raspberry Pi DHT11 Temperature test program\n")

            time.sleep(1)       
            # read the humidity & temperature
            for i in range(0,10):
                humidity, temperature = read_dht11_dat()
                # GPIO.cleanup()

                payload_json = {
                    'id': int(time.time()),
                    'params': {
                        'temperature': temperature, # 
                        'humidity': humidity, # 
                    },
                    'method': "thing.event.property.post"
                }
                print('send data to iot server: ' + str(payload_json))

                client.publish(PUB_TOPIC,payload=str(payload_json),qos=1)
                # client.loop_forever()

                time.sleep(5)

        except KeyboardInterrupt:
            GPIO.cleanup()
