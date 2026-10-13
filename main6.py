from machine import Pin, PWM
import time
import network
from umqtt.simple import MQTTClient

WIFI_SSID = "TskoliVESM"   
WIFI_PASSWORD = "Fallegurhestur" 
MQTT_BROKER = "test.mosquitto.org"

SERVO1_PAN_PIN = 13  
SERVO2_TILT_PIN = 15   


pan_servo = PWM(Pin(SERVO1_PAN_PIN), freq=50)
tilt_servo = PWM(Pin(SERVO2_TILT_PIN), freq=50)

def set_servo_angle(servo_obj, angle):
    if angle < 0: angle = 0
    if angle > 180: angle = 180
    ns_value = int(500000 + (angle / 180) * 2000000)
    servo_obj.duty_ns(ns_value)

print("Aligning servos to default 90° center alignment positions...")
set_servo_angle(pan_servo, 90)
set_servo_angle(tilt_servo, 90)


wlan = network.WLAN(network.STA_IF)
wlan.active(False)     
time.sleep(0.5)       
wlan.active(True)       
wlan.disconnect()       
time.sleep(0.5)

wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(0.5)
print("WiFi Connected! Assigned Local IP Unit:", wlan.ifconfig()[0])


def mqtt_callback(topic, msg):
    topic_str = topic.decode()
    msg_str = msg.decode()
    print(f"Received Inbound MQTT Action -> Topic: {topic_str}, Message: {msg_str}")
    
    try:
        angle = int(msg_str)
        if topic_str == "weather/servo1":
            set_servo_angle(pan_servo, angle)
        elif topic_str == "weather/servo2":
            set_servo_angle(tilt_servo, angle)
    except ValueError:
        print("Invalid numerical payload parsed. Dropping transmission packet.")

client = MQTTClient("FreenoveS3Mount", MQTT_BROKER)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe("weather/servo1")
client.subscribe("weather/servo2")
print("Connected to test.mosquitto.org! Listening for NiceGUI movements...")

while True:
    try:
        client.check_msg()
        time.sleep(0.05)
    except OSError:
        print("Network packet stream interrupted. Attempting MQTT link recovery...")
        time.sleep(5)
        try:
            client.connect()
            client.subscribe("weather/servo1")
            client.subscribe("weather/servo2")
            print("MQTT Connection successfully restored!")
        except Exception as e:
            print("Reconnection loop stalled. Retrying shortly...")

