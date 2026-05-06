import RPi.GPIO as GPIO
import time

TRIG = 5
ECHO = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance_cm():
    GPIO.output(TRIG, False)
    time.sleep(0.002)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - start > 0.1:
            return None
        start = time.time()

    stop = time.time()
    while GPIO.input(ECHO) == 1:
        if time.time() - stop > 0.1:
            return None
        stop = time.time()

    elapsed = stop - start
    return (elapsed * 34300) / 2  # Speed of sound