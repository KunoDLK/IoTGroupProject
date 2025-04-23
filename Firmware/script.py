import json
import time
import spidev
from dataclasses import dataclass, asdict
import paho.mqtt.client as mqtt

@dataclass
class SensorData:
    FillLevel: int
    Weight: float
    Desnsity: float

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
sensor_topic = "Sensors/Current"
full_topic = f"{root_topic}/{sensor_topic}"

client.username_pw_set(mqtt_user, mqtt_password)
client.tls_set()  # << Required for port 8883

print("Starting connection to MQTT")
client.connect(mqtt_broker, mqtt_port)
client.loop_start()
print("Connected to MQTT")

while True:
    weightPercentage = (weightReader.read_channel(0) / 750.0) * 100
    data = SensorData(100, int(round(weightPercentage)), 10)
    payload = json.dumps(asdict(data))
    
    start = time.time()
    info = client.publish(full_topic, payload, qos=2)
    info.wait_for_publish()
    end = time.time()
    print(f"Sent data in {end - start:.3f} seconds")
    time.sleep(0.25)