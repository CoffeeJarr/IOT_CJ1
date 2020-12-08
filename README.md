# IOT_CJ1 
### Descriptions  
  1. Record the process of the final project.  
  2. Study to use the GitHub since it's my first time.  
  3. Record the study of the Pyhton and Raspberry Pi 4B.  
### Weekly Reports & Labs
  1. Record weekly studies about the Internet of Things and RaspberryPi.   
  2. Record the replications and attempts of each labs.  
### Final Project  
  **Title**: Online air conditioning control system based on Aliyun and RaspberryPi.  
  **Main idea**: Based on the temperature and humidity sensor and infrared receiver and transmitter on the RaspberryPi, real-time indoor temperature and humidity are controlled through Aliyun platform, and real-time temperature control is realized through Aliyun webpage.  
  **Steps**:  
  1. Use DHT11 to obtain indoor temperature and humidity.  
  2. Transmit the acquired data to Aliyun platform.  
  3. Use the infrared receiver to unencode the corresponding instruction code of the air conditioning remote control and set corresponding commands.  
  4. Send commands on Aliyun platform, and use the infrared transmitter connected with RaspberryPi to send commands to control the adjustment of temperature and humidity of air conditioning.  

**Code**:  
  1. connect_dht11_aliyun.py # use dht11, get connection to the aliyun, and send the temperature and humidity data to the web.   
  2. connect_dht22_aliyun.py # use dht22, get connection to the aliyun, and send the temperature and humidity data to the web.   
  3. connect_ir_aliyun.py    # use 38khz ir receiver and transmitter, get connection to the aliyun, and send LED status to the web.   
