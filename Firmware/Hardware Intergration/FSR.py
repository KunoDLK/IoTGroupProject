import spidev
import time

# Create SPI object
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0 (GPIO 8)
spi.max_speed_hz = 1350000

def read_channel(channel):
    if not 0 <= channel <= 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

try:
    while True:
        value = read_channel(0)
        voltage = value * 3.3 / 1023  # Assuming Vref = 3.3V
        print(f"Channel 0: {value} (~{voltage:.2f} V)")
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
    print("Stopped")