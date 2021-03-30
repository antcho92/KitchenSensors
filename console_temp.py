import adafruit_dht
import paho.mqtt.client as paho
import os
import time
import RPi.GPIO as GPIO
import board

# --------- User Settings ---------
SENSOR_LOCATION_NAME = "Bedroom"
MINUTES_BETWEEN_READS = 1
METRIC_UNITS = True
# ---------------------------------

dhtSensor = adafruit_dht.DHT22(board.D4)

while True:
    try:
        humidity = dhtSensor.humidity
        temp_c = dhtSensor.temperature
    except RuntimeError:
        print("RuntimeError, trying again...")
        continue
            
    if METRIC_UNITS:
        print(f'{SENSOR_LOCATION_NAME} Temperature({temp_c})')
    else:
        temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
        print(f'{SENSOR_LOCATION_NAME} Temperature({temp_f})')
    humidity = format(humidity,".2f")
    print(f'{SENSOR_LOCATION_NAME}  Humidity(%)({humidity})')
    time.sleep(60*MINUTES_BETWEEN_READS)