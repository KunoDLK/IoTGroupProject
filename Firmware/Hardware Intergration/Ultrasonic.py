import adafruit_dht
import board

dht_device = adafruit_dht.DHT11(board.D14)

try:
    temperature = dht_device.temperature
    humidity = dht_device.humidity
except RuntimeError as e:
    print(f"DHT error: {e}")
    temperature = None
    humidity = None