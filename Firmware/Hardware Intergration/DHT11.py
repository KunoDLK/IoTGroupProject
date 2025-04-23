from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=17, trigger=27)

try:
    while True:
        distance_cm = sensor.distance * 100
        print(f"Distance: {distance_cm:.1f} cm")
except KeyboardInterrupt:
    print("Stopped")