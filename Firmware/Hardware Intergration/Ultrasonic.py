import gpiozero as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
TRIG = 17
ECHO = 27
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

try:
    while True:
        # Send trigger pulse
        GPIO.output(TRIG, True)
        time.sleep(0.00001)  # 10 µs pulse
        GPIO.output(TRIG, False)

        # Wait for echo start
        while GPIO.input(ECHO) == 0:
            start = time.time()

        # Wait for echo end
        while GPIO.input(ECHO) == 1:
            end = time.time()

        # Calculate distance (speed of sound = 34300 cm/s)
        duration = end - start
        distance = (duration * 34300) / 2

        print(f"Distance: {distance:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped by User")

finally:
    GPIO.cleanup()