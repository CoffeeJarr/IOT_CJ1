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

DHTPIN = 4         #引脚号17

GPIO.setmode(GPIO.BCM)      #以BCM编码格式

def read_dht11_dat():
    
    GPIO.setup(DHTPIN, GPIO.OUT)
    GPIO.output(DHTPIN, GPIO.LOW)
    #给信号提示传感器开始工作,并保持低电平18ms以上
    time.sleep(0.002)                #这里保持20ms   
    # GPIO.output(DHTPIN, GPIO.HIGH)  #然后输出高电平
    # GPIO.output(DHTPIN, GPIO.LOW)  #然后输出高电平    

    GPIO.setup(DHTPIN, GPIO.IN)    
    # 发送完开始信号后得把输出模式换成输入模式，不然信号线上电平始终被拉高
 
    while GPIO.input(DHTPIN) == GPIO.LOW:
        continue
    #DHT11发出应答信号，输出 80 微秒的低电平
    
    while GPIO.input(DHTPIN) == GPIO.HIGH:
        continue
    #紧接着输出 80 微秒的高电平通知外设准备接收数据


    #开始接收数据
    j = 0               #计数器
    data = []           #收到的二进制数据
    kk=[]               #存放每次高电平结束后的k值的列表
    while j < 40:
        k = 0
        while GPIO.input(DHTPIN) == GPIO.LOW:  # 先是 50 微秒的低电平、
            continue
        while GPIO.input(DHTPIN) == GPIO.HIGH: # 接着是26-28微秒的高电平，或者 70 微秒的高电平
            k += 1
            if k > 100:
                break
        kk.append(k)
        if k < 20:       #26-28 微秒时高电平时通常k等于5或6
            data.append(0)      #在数据列表后面添加一位新的二进制数据“0”
        else:           #70 微秒时高电平时通常k等于17或18
            data.append(1)      #在数据列表后面添加一位新的二进制数据“1”
 
        j += 1
 
    print("sensor is working.")
    print('初始数据高低电平:\n',data)    #输出初始数据高低电平
    print('参数k的列表内容：\n',kk)      #输出高电平结束后的k值
    
    m = np.logspace(15,0,16,base=2,dtype=int) #logspace()函数用于创建一个于等比数列的数组
    #即[128 64 32 16 8 4 2 1]，8位二进制数各位的权值
    data_array = np.array(data) #将data列表转换为数组

    #dot()函数对于两个一维的数组，计算的是这两个数组对应下标元素的乘积和(数学上称之为内积)
    humidity = m.dot(data_array[0:16])           #用前8位二进制数据计算湿度的十进制值
    # humidity_point = m.dot(data_array[8:16])
    temperature = m.dot(data_array[16:32])
    # temperature_point = m.dot(data_array[24:32])
    # check = m.dot(data_array[32:40])
    
    print(humidity,temperature)
    
    # tmp = humidity + humidity_point + temperature + temperature_point
    #十进制的数据相加

    return humidity, temperature
    # if check == tmp:    #数据校验，相等则输出
    #     return humidity, temperature
    # else:               #错误输出错误信息
    #     return False



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

            time.sleep(1)           #通电后前一秒状态不稳定，时延一秒
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


