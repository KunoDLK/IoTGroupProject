import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
TRIG = 27
ECHO = 17
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Send trigger pulse
    
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10µs pulse
    GPIO.output(TRIG, False)


    # Wait for echo start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    # Wait for echo end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound divided by two (back and forth)
    distance = round(distance, 2)
    
    return distance

import time

try:
    lastPrintedDist = -100.0
    lastPrintTime = time.time()

    while True:
        dist = get_distance()
        currentTime = time.time()

        if abs(dist - lastPrintedDist) > 5:
            print(f"Distance: {dist:.2f} cm")
            lastPrintedDist = dist
            lastPrintTime = currentTime
        elif currentTime - lastPrintTime >= 0.25:
            print(f"Distance: {dist:.2f} cm")
            lastPrintedDist = dist
            lastPrintTime = currentTime

        time.sleep(0.05)  # 10ms

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()