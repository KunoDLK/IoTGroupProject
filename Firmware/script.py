from __future__ import absolute_import, division, print_function, unicode_literals
import json
import time
import threading
import time
import pigpio
import math
import spidev
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from dataclasses import dataclass, asdict

binDepth = 0.25
binWidth = 0.15
binEmptyWeight = 0.5
lat = 54.523869
lon = -1.3515934

@dataclass
class SensorData:
    FillLevel: int
    Weight: float
    Density: float
    Latitude: float
    Longitude: float

@dataclass
class EnvironmentData:
    Temperature: int
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
    
    def read_weight(self, channel):
        adc_value = weightReader.read_channel(channel)
        voltage = (adc_value / 1024.0) * 5.0  # Convert ADC count to voltage
        return (0.2 * math.exp(voltage)) - binEmptyWeight  # Since a=1 and b=1, F = e^(V)

    def close(self):
        self.spi.close()

class DHT11(object):
    """
    The DHT11 class is a stripped version of the DHT22 sensor code by joan2937.
    """

    def __init__(self, pi, gpio):
        """
        pi (pigpio): an instance of pigpio
        gpio (int): gpio pin number
        """
        self.pi = pi
        self.gpio = gpio
        self.high_tick = 0
        self.bit = 40
        self.temperature = 0
        self.humidity = 0
        self.either_edge_cb = None
        self.setup()

    def setup(self):
        """
        Clears the internal gpio pull-up/down resistor.
        Kills any watchdogs.
        """
        self.pi.set_pull_up_down(self.gpio, pigpio.PUD_OFF)
        self.pi.set_watchdog(self.gpio, 0)
        self.register_callbacks()

    def register_callbacks(self):
        """
        Monitors RISING_EDGE changes using callback.
        """
        self.either_edge_cb = self.pi.callback(
            self.gpio,
            pigpio.EITHER_EDGE,
            self.either_edge_callback
        )

    def either_edge_callback(self, gpio, level, tick):
        """
        Either Edge callbacks, called each time the gpio edge changes.
        Accumulate the 40 data bits from the dht11 sensor.
        """
        level_handlers = {
            pigpio.FALLING_EDGE: self._edge_FALL,
            pigpio.RISING_EDGE: self._edge_RISE,
            pigpio.EITHER_EDGE: self._edge_EITHER
        }
        handler = level_handlers[level]
        diff = pigpio.tickDiff(self.high_tick, tick)
        handler(tick, diff)

    def _edge_RISE(self, tick, diff):
        """
        Handle Rise signal.
        """
        val = 0
        if diff >= 50:
            val = 1
        if diff >= 200:  # Bad bit?
            self.checksum = 256  # Force bad checksum

        if self.bit >= 40:  # Message complete
            self.bit = 40
        elif self.bit >= 32:  # In checksum byte
            self.checksum = (self.checksum << 1) + val
            if self.bit == 39:
                # 40th bit received
                self.pi.set_watchdog(self.gpio, 0)
                total = self.humidity + self.temperature
                # Is checksum ok?
        elif 16 <= self.bit < 24:  # In temperature byte
            self.temperature = (self.temperature << 1) + val
        elif 0 <= self.bit < 8:  # In humidity byte
            self.humidity = (self.humidity << 1) + val
        else:
            pass  # Skip header bits
        self.bit += 1

    def _edge_FALL(self, tick, diff):
        """
        Handle Fall signal.
        """
        self.high_tick = tick
        if diff <= 250000:
            return
        # Start of new message
        self.bit = -2
        self.checksum = 0
        self.temperature = 0
        self.humidity = 0

    def _edge_EITHER(self, tick, diff):
        """
        Handle Either signal.
        """
        self.pi.set_watchdog(self.gpio, 0)

    def read(self):
        """
        Start reading over DHT11 sensor.
        """
        self.pi.write(self.gpio, pigpio.LOW)
        time.sleep(0.017)  # 17 ms
        self.pi.set_mode(self.gpio, pigpio.INPUT)
        self.pi.set_watchdog(self.gpio, 200)
        time.sleep(0.2)

    def close(self):
        """
        Stop reading sensor, remove callbacks.
        """
        self.pi.set_watchdog(self.gpio, 0)
        if self.either_edge_cb:
            self.either_edge_cb.cancel()
            self.either_edge_cb = None

    def __iter__(self):
        """
        Support the iterator protocol.
        """
        return self

    def __next__(self):
        """
        Call the read method and return temperature and humidity information.
        """
        self.read()
        response = {
            'humidity': self.humidity,
            'temperature': self.temperature
        }
        return response

    # For Python 2 compatibility (optional)
    next = __next__

class UltrasonicSensor:
    def __init__(self, trig_pin=27, echo_pin=17):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        # Send trigger pulse
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)  # 10µs pulse
        GPIO.output(self.trig_pin, False)

        # Wait for echo start
        pulse_start = time.time()
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()

        # Wait for echo end
        pulse_end = time.time()
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 171.50  # m
        distance = round(distance, 3)
        return distance

    def cleanup(self):
        GPIO.cleanup()

def sensor_loop():
    radius = binWidth / 2
    binVolume = math.pi * (radius ** 2) * binDepth

    while True:
        weight = weightReader.read_weight(0)  # Kg
        fillPercentage = ((binDepth - fillSensor.get_distance()) / binDepth) * 100

        if fillPercentage > 10:
            filledVolume = binVolume * (fillPercentage / 100)
            density = weight / filledVolume  # Kg per unit³
        else:
            density = 0  # or another fallback

        data = SensorData(round(fillPercentage, 1), round(weight, 1), round(density, 1), round(lat, 3), round(lon, 3))
        payload = json.dumps(asdict(data))
        print(data)

        client.publish(sensors_topic, payload, qos=2)
        time.sleep(300)

def weather_loop():
    while True:

        sensorData = next(weatherSensor)
        data = EnvironmentData(int(sensorData['temperature']),int(sensorData['humidity']))
        payload = json.dumps(asdict(data))
        print(data)
        
        client.publish(environment_topic, payload, qos=2)
        time.sleep(900)


client = mqtt.Client()
weightReader = ADCReader()
pi = pigpio.pi()
weatherSensor = DHT11(pi, 4)  # GPIO4
fillSensor = UltrasonicSensor()

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