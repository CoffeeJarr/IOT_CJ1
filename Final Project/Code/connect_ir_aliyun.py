#!/usr/bin/env python
import RPi.GPIO as GPIO
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

#这个就是我们在阿里云注册产品和设备时的三元组啦
#把我们自己对应的三元组填进去即可
options = {
    'productKey':'###',
    'deviceName':'###',
    'deviceSecret':'###',
    'regionId':'cn-shanghai'
}


IrPin  = 11
LedPin = 12

Led_status = 1

GPIO.setmode(GPIO.BCM)      #以BCM编码格式

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(IrPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(LedPin, GPIO.LOW) # Set LedPin high(+3.3V) to off led

def swLed(ev=None):
    global Led_status
    Led_status = not Led_status
    GPIO.output(LedPin, Led_status)  # switch led status(on-->off; off-->on)
    if Led_status == 1:
        print 'led on...'
    else:
        print '...led off'

def loop():
    GPIO.add_event_detect(IrPin, GPIO.FALLING, callback=swLed) # wait for falling
    while True:
        pass   # Don't do anything

def destroy():
    GPIO.output(LedPin, GPIO.LOW)     # led off
    GPIO.cleanup()                     # Release resource



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

            for i in range(0,10):
                # GPIO.cleanup()

                payload_json = {
                    'id': int(time.time()),
                    'params': {
                        'led': Led_status # 
                    },
                    'method': "thing.event.property.post"
                }
                print('send data to iot server: ' + str(payload_json))

                client.publish(PUB_TOPIC,payload=str(payload_json),qos=1)
                # client.loop_forever()

                time.sleep(5)

        except KeyboardInterrupt:
            GPIO.cleanup()
