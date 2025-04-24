import json
import time
import threading
import requests
import spidev
from dataclasses import dataclass, asdict
import paho.mqtt.client as mqtt

@dataclass
class SensorData:
    FillLevel: int
    Weight: float
    Desnsity: float

@dataclass
class EnvironmentData:
    Temp: int
    Humidity: int

class ADCReader:
    def __init__(self, bus=0, device=0, speed=1350000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = speed

    def read_channel(self, channel):
        if not 0 <= channel <= 7:
            return -1
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        value = ((adc[1] & 3) << 8) + adc[2]
        return value

    def close(self):
        self.spi.close()

class Weather:
    def __init__(self, city='Middlesbrough'):
        self.city = city

    def GetTemp(self):
        url = f'https://wttr.in/{self.city}?format=%t'
        response = requests.get(url)
        return response.text.strip()
    
    def GetHumidity(self):
        url = f'https://wttr.in/{self.city}?format=%h'
        response = requests.get(url)
        return response.text.strip()


def sensor_loop():
    while True:
        weightPercentage = (weightReader.read_channel(0) / 750.0) * 100
        fillPercentage = weightPercentage
        
        if fillPercentage > 0.0:
            density = weightPercentage / fillPercentage
        else:
            density = 1  # or handle it another way

        data = SensorData(int(round(weightPercentage)), int(round(weightPercentage)), int(round(density)))
        payload = json.dumps(asdict(data))
        
        client.publish(sensors_topic, payload, qos=2)
        time.sleep(10)


def weather_loop():
    weather = Weather()

    while True:
        data = EnvironmentData(weather.GetTemp(), weather.GetHumidity())
        payload = json.dumps(asdict(data))
        
        client.publish(environment_topic, payload, qos=2)
        time.sleep(60)


client = mqtt.Client()
weightReader = ADCReader()

mqtt_broker = "c79e2ea5e65e40f6b79ba3a3aad7c19f.s1.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_user = "admin"
mqtt_password = "Password1"

Area = "TS16"
Street = "Formby_walk"
House = 1

root_topic = f"{Area}/{Street}/{House}"
sensor_topic_extension = "Sensors"
environment_topic_extension = "Environment"
realtime_topic_extension = "Current"
sensors_topic = f"{root_topic}/{sensor_topic_extension}/{realtime_topic_extension}"
environment_topic = f"{root_topic}/{environment_topic_extension}/{realtime_topic_extension}"

client.username_pw_set(mqtt_user, mqtt_password)
client.tls_set()  # << Required for port 8883

print("Starting connection to MQTT")
client.connect(mqtt_broker, mqtt_port)
client.loop_start()
print("Connected to MQTT")

sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
sensor_thread.start()

weather_loop()