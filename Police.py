# thanks to https://github.com/MikeTeachman/micropython-adafruit-mqtt-esp8266/blob/master/mqtt-to-adafruit.py
#

import network
import time
import machine
from servo import Servo
from umqtt.simple import MQTTClient

pin = machine.Pin(13, machine.Pin.OUT) # LED on the board
button = machine.Pin (34, machine.Pin.IN)
led = machine.Pin(26, machine.Pin.OUT) # LED on the board
servo_pin1 = machine.Pin(4)
my_servo1 = Servo(servo_pin1)
my_servo1.write_angle(0)
headcount = 0

def sub_cb(topic, msg):
    value = float(str(msg,'utf-8'))
    print("subscribed value = {}".format(value))
    if value > 4:
        pin.value(1)
    else:
        pin.value(0)

# connect the ESP to local wifi network
yourWifiSSID = ""
yourWifiPassword = ""
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    sta_if.active(True)
    sta_if.connect(yourWifiSSID, yourWifiPassword)
    while not sta_if.isconnected():
        pass
print("connected to WiFi")

# connect ESP to Adafruit IO using MQTT
myMqttClient = ""  
adafruitUsername = ""  
adafruitAioKey = ""  
adafruitFeed = adafruitUsername + "/feeds/mydata" 
adafruitIoUrl = "io.adafruit.com"

c = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
c.set_callback(sub_cb)
c.connect()
c.subscribe(bytes(adafruitFeed,'utf-8'))


while True:
    if button.value() == 1:
        led.value(1)
        time.sleep(10)
        headcount = headcount + 1
        print ("Current headcount: ", headcount)
        c.publish(adafruitFeed,str(headcount))
        c.check_msg()
        for i in range(0,180,1):
          if i == 60 or i == 120 or i == 180 :
              time.sleep(5)
          else:
              my_servo1.write_angle(i)
              time.sleep(0.16)
        print("servo turning!")
        for i in range(180,-1,-1):
              my_servo1.write_angle(i)
              time.sleep(0.025)
        print("servo backing up!")

    else:
        led.value(0)
    time.sleep(1.0)

c.disconnect()

