# humidityTemperatureMQTT.py (c) Jonathan Haddock, @joncojonathan, 2020

# Adapted from https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/ 
# also using guidance from https://appcodelabs.com/introduction-to-iot-build-an-mqtt-server-using-raspberry-pi
# and http://www.steves-internet-guide.com/into-mqtt-python-client/
# Many thanks!

import adafruit_dht
import paho.mqtt.client as paho
import os
import time
import RPi.GPIO as GPIO
import board

# Define constants
# Sensor type (Adafruit_DHT.DHT11 or Adafruit_DHT.DHT22)
DHT_SENSOR = Adafruit_DHT.DHT22

# Configure GPIO pins
PIN_ONE = 4
PIN_TWO = 17

# MQTT details
MQTT_BROKER="127.0.0.1"
MQTT_PORT=1883

# Output file name
LOGFILE = "/home/pi/sensors.csv"

##########################################################
# Only edit below if you know what you're doing!
##########################################################

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
client1= paho.Client("control1")                    #create client object
client1.on_publish = on_publish                     #assign function to callback
client1.connect(MQTT_BROKER,MQTT_PORT)              #establish connection

try:
    f = open(LOGFILE, 'a+')
    if os.stat(LOGFILE).st_size == 0:
            f.write('Date,Time,Sensor,Temperature,Humidity\r\n')
except:
    pass

channel_list = [PIN_ONE, PIN_TWO]
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel_list, GPIO.IN)
GPIO.add_event_detect(channel_list, GPIO.BOTH)

cupboardHumidity, cupboardTemperature = Adafruit_DHT.read_retry(DHT_SENSOR, PIN_ONE)

floorHumidity, floorTemperature = Adafruit_DHT.read_retry(DHT_SENSOR, PIN_TWO)

    
if cupboardHumidity is not None and cupboardTemperature is not None:
    ret= client1.publish("kitchen/cupboard/temperature","{0:0.1f}".format(cupboardTemperature))
    ret= client1.publish("kitchen/cupboard/humidity","{0:0.1f}".format(cupboardHumidity))
    f.write('{0},{1},Cupboard,{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%y-%m-%d'), time.strftime('%H:%M'), cupboardTemperature, cupboardHumidity))
else:
    ret= client1.publish("kitchen/cupboard/temperature","FAILED")
    print("Failed to retrieve data from cupboard sensor")

if floorHumidity is not None and floorTemperature is not None:
    ret= client1.publish("kitchen/floor/temperature","{0:0.1f}".format(floorTemperature))
    ret= client1.publish("kitchen/floor/humidity","{0:0.1f}".format(floorHumidity))
    f.write('{0},{1},Floor,{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%y-%m-%d'), time.strftime('%H:%M'), floorTemperature, floorHumidity))
else:
    ret= client1.publish("kitchen/floor/temperature","FAILED")
    print("Failed to retrieve data from floor sensor")

# if washingMachineHumidity is not None and washingMachineTemperature is not None:
#     ret= client1.publish("kitchen/washing-machine/temperature","{0:0.1f}".format(washingMachineTemperature))
#     ret= client1.publish("kitchen/washing-machine/humidity","{0:0.1f}".format(washingMachineHumidity))
#     f.write('{0},{1},Washing-Machine,{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%y-%m-%d'), time.strftime('%H:%M'), washingMachineTemperature, washignMachineHumidity))
# else:
#     ret= client1.publish("kitchen/washing-machine/temperature","FAILED")
#     print("Failed to retrieve data from washing-machine sensor")

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")
client1.on_disconnect = on_disconnect
client1.disconnect()
