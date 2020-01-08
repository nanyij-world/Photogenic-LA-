# thanks to https://github.com/MikeTeachman/micropython-adafruit-mqtt-esp8266/blob/master/mqtt-to-adafruit.py
#
yourWifiSSID = ""
yourWifiPassword = ""
def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(yourWifiSSID, yourWifiPassword)
        # while the below while loop is part of the standard recommended approach,
        # I found it could hang the device if run with connect() on boot
        # while not sta_if.isconnected():
        #     pass
    print('network config:', sta_if.ifconfig())

def showip():
    import network
    sta_if = network.WLAN(network.STA_IF)
    print('network config:', sta_if.ifconfig())

connect()

import network
import time
import machine
from servo import Servo
from umqtt.simple import MQTTClient

pin = machine.Pin(13, machine.Pin.OUT) # LED on the board
led = machine.Pin(26, machine.Pin.OUT)
adc = machine.ADC(machine.Pin(34))
adc.atten(machine.ADC.ATTN_11DB)
servo_pin = machine.Pin(4)
my_servo = Servo(servo_pin)
my_servo.write_angle(0)


def sub_cb(topic, msg):
    value = float(str(msg,'utf-8'))
    print("subscribed value = {}".format(value))
    while value < 3:
        led.value(1)
        time.sleep(0.7)
        led.value(0)
        my_servo.write_angle(30)
        time.sleep(0.5)
        my_servo.write_angle(25)
        print (adc.read())
        if adc.read() > 0:
            my_servo.write_angle(90)
            time.sleep(2)
        c.check_msg()
    
    while value >= 3 and value <5:
        led.value(1)
        time.sleep(0.4)
        led.value(0)
        my_servo.write_angle(60)
        time.sleep(0.3)
        my_servo.write_angle(55)
        print (adc.read())
        if adc.read() > 0:
            my_servo.write_angle(90)
            time.sleep(2)
        c.check_msg()

    while value >= 5:
        led.value(1)
        time.sleep(0.2)
        led.value(0)
        my_servo.write_angle(90)
        time.sleep(0.1)
        my_servo.write_angle(85)
        c.check_msg()

    while value == 0:
        led.value(0)
        c.check_msg()
        
# connect the ESP to local wifi network
#
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
#
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
    print ("check message ")
    c.check_msg()
    time.sleep(2)

c.disconnect()

