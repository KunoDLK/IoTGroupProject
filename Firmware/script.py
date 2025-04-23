import json
import time
from dataclasses import dataclass, asdict
import paho.mqtt.client as mqtt

@dataclass
class SensorData:
    FillLevel: int
    Weight: float
    Desnsity: float

client = mqtt.Client()

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

data = SensorData(100, 50.0, 10)
payload = json.dumps(asdict(data))

while True:
    start = time.time()
    info = client.publish(full_topic, payload, qos=2)
    info.wait_for_publish()
    end = time.time()
    print(f"Sent test data in {end - start:.3f} seconds")
    time.sleep(1)