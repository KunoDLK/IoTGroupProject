import spidev

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


import time
import math

weightReader = ADCReader()
lastPrintedWeight = -100.0
lastPrintTime = time.time()

try:
    while True:
        adc_value = weightReader.read_channel(0)
        voltage = (adc_value / 1024.0) * 5.0  # Convert ADC count to voltage
        weight =  0.2 * math.exp(voltage)   # Since a=1 and b=1, F = e^(V)

        currentTime = time.time()
        
        if abs(weight - lastPrintedWeight) > 1:
            print("Weight: {:.2f}KG".format(weight))
            lastPrintedWeight = weight
            lastPrintTime = currentTime
        elif currentTime - lastPrintTime >= 0.5:
            print("Weight: {:.2f}KG".format(weight))
            lastPrintedWeight = weight
            lastPrintTime = currentTime

        time.sleep(0.05)  # 10ms

except KeyboardInterrupt:
    print("\nProgram stopped by user.")