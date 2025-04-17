import time
import json
import random
import paho.mqtt.client as mqtt

# === MQTT CONFIG ===
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
CLIENT_ID = 'raspi-sensor-node'

# === LOCATION INFO ===
POSTCODE = 'TS16'
STREET = 'FORMBY_WALK'
HOUSE_NUM = '01'

BASE_TOPIC = f"{POSTCODE}/{STREET}/{HOUSE_NUM}"

# === TIMING ===
READ_INTERVAL_SECONDS = 3600  # Once per hour


# === MQTT SETUP ===
def connect_mqtt():
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311, transport="tcp", callback_api_version=5)
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client


# === SENSOR READINGS (replace with real sensors) ===
def read_sensor_data():
    return {
        "fillLevel": random.randint(0, 100),
        "weight": round(random.uniform(10.0, 20.0), 2),
        "density": round(random.uniform(1.0, 2.0), 2)
    }


def read_environment_current():
    return {
        "temp": round(random.uniform(15.0, 25.0), 1),
        "humidity": random.randint(40, 70)
    }


def read_environment_daily():
    low = round(random.uniform(5.0, 10.0), 1)
    high = round(random.uniform(20.0, 25.0), 1)
    return {
        "low": low,
        "high": high
    }


# === PUBLISH FUNCTION ===
def publish_data(mqtt_client, topic, data):
    json_payload = json.dumps(data)
    print(f"Publishing to {topic}: {json_payload}")
    mqtt_client.publish(topic, json_payload)


# === MAIN LOOP ===
def main():
    mqtt_client = connect_mqtt()
    print("MQTT connected. Starting hourly data reporting...")

    while True:
        # Sensor Data
        sensor_data = read_sensor_data()
        publish_data(mqtt_client, f"{BASE_TOPIC}/Sensors/Current", sensor_data)

        # Environment Data
        env_current = read_environment_current()
        publish_data(mqtt_client, f"{BASE_TOPIC}/Environment/Current", env_current)

        # Daily Summary
        env_daily = read_environment_daily()
        publish_data(mqtt_client, f"{BASE_TOPIC}/Environment/Daily", env_daily)

        # Wait 1 hour
        time.sleep(READ_INTERVAL_SECONDS)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
