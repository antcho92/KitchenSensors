
import adafruit_dht
import paho.mqtt.client as paho
import os
import time
import RPi.GPIO as GPIO
import board

# --------- User Settings ---------
SENSOR_1 = "Sensor 1"
SENSOR_2 = "Sensor 2"
MINUTES_BETWEEN_READS = 1
METRIC_UNITS = True
# ---------------------------------

dhtSensor = adafruit_dht.DHT22(board.D4)
s2 = adafruit_dht.DHT22(board.D17)

while True:
    try:
        humidity = dhtSensor.humidity
        temp_c = dhtSensor.temperature

        h2 = s2.humidity
        t2 = s2.temperature

        if h2 is None or t2 is None:
            print("h2 or t2 is null. Reconnect and try again.")
    except RuntimeError:
        print("RuntimeError, trying again...")
        continue

    temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
    t2_f = format(t2 * 9.0 / 5.0 + 32.0, ".2f")
    print(f'{SENSOR_1}: Temperature: {temp_c} degrees celsius, {temp_f} degrees fahrenheit')
    print(f'{SENSOR_2}: Temperature: {temp_c} degrees celsius, {temp_f} degrees fahrenheit')

    humidity = format(humidity, ".2f")
    humidity2 = format(h2, ".2f")
    print(f'{SENSOR_1}: Humidity(%)({humidity})')
    print(f'{SENSOR_2}:  Humidity(%)({h2})')
    time.sleep(60*MINUTES_BETWEEN_READS)
