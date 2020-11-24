##### IOT_CJ1  
  1. Record the process of the final project  
  2. Study to use the github since it's my first time  
  3. Record the study of the Pyhton and Raspberry Pi 4B  

###### [Weekly Reports]
  **Tenth week**    
  [2020-11-21]  
  Change DHT11 to DHT22, improve the detection accuracy of temperature and humidity, modify the corresponding function, and realize that two kinds of sensors can be called at     the same time, and the accuracy of the two can be compared in the background 
  [2020-11-17]  
  Try to start the automatic connection between RaspberryPi and Aliyun when starting up. There is a slight problem and it is being solved  
  **Ninth week**    
  [2020-11-12]  
  Continue to improve the types of commands sent from Aliyun to RaspberryPi, and realize the function of temperature control after the air conditioning is turned on 
  [2020-11-09]  
  Try sending commands to the RaspberryPi from Aliyun, and then indirectly control the infrared emission, Realize the function of turning on and off the air conditioner      
  **Eigth week**    
  [2020-11-03]  
  The infrared signal transmitter successfully transmitted from the RaspberryPi, and can controled through the signal from Aliyun      
  [2020-11-01]  
  The infrared signal receiver successfully connected to Aliyun  
  **Seventh week**    
  [2020-10-26]  
  Try to build a UI to check the room temperature and humidity  
  [2020-10-25]  
  The real-time temperature and humidity data collected by DHT11 is sent by Raspberry Pi to Aliyun platform successfully, and is set to be updated every 5 seconds  
  [2020-10-23]  
  Equipped with a 38KHZ universal infrared receiver and transmitter module  
  **Sixth week**  
  [2020-10-17]  
  The RaspberryPi successfully connected to the camera and realized video and photo functions, next step: try to connect to the Aliyun to show the video  
  [2020-10-15]  
  Use Winscp to make the Windows and Linux transfer files freely    
  Use Synergy to make my desktop and RaspberryPi share the same mouse and keyboard , also the set RaspberryPi to start Synergy automatically when power-on  
  [2020-10-14]   
  Purchase MB-102 bread boards and various dupont lines and corresponding power modules
  New Development Steps:
    1. Install LIRC (LINUX infrared remote control) for Raspberry Pi  
    2. Register Aliyun account and open the Aliyun Internet of Things platform  
      a. Raspberry PI as device accessed: Device platform: Linux; Device connection protocol: MQTT; Device development kit: Node.js  
      b. Download python3 and SDK for Raspberry Pi  
      c. Use the python example scripts which is offered by Aliyun website, modify Aliyun platform's ProductKey/DeviceSecret/DeviceName, run the program, successfully connect the Aliyun  
    3. Connecting the same mouse system back and forth between the raspberry PI and my laptop was a hassle, so I chose to try sharing the keyboard mouse between computers. Synergy maybe a good way to help to share the keyboard mouse and the clipboard    
  **Fifth week**  
    The creation of mind maps;  
    The functions and tasks of each module are specified;  
    The ultimate target of the project is to use the Siri assistant of IOS to remotely control the air conditioner.    
  **Fourth week**  
    Install the raspberry PI system, purchase the corresponding temperature sensor, humidity sensor, infrared receiving and sending equipment, familiar with their control situation.   
  **Third week**  
    Using raspberry PI as a controller for air conditioning which can be operated remotely through Internet. Besides, it can collect the actual indoor temperature and humidity, and adjust 
    different strategies to control the temperature, humidity and wind speed in different states, so as to achieve the best real-time control state  
  **Second week**  
    purchase the Raspberry Pi 4B with a camera and a display screen  
    try to use the Raspberry Pi and call the camera, since I used to be familiar with C++ and matlab in the past , maybe I still need some time to grasp the Python  
  **First week**  
    learn to use the github and have a general understanding of IOT  
