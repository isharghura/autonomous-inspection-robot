import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# motor A (left side), connected to L298N #1
IN1, IN2, ENA = 17, 27, 18
# motor B (right side), connected to L298N #2  
IN3, IN4, ENB = 22, 23, 24

for pin in [IN1, IN2, ENA, IN3, IN4, ENB]:
    GPIO.setup(pin, GPIO.OUT)

pwm_a = GPIO.PWM(ENA, 1000)  # 1kHz pwm
pwm_b = GPIO.PWM(ENB, 1000)
pwm_a.start(0)
pwm_b.start(0)

# Speed: -100 to 100. Negative = reverse
def set_motors(left_speed, right_speed):
    # left motor
    GPIO.output(IN1, left_speed > 0)
    GPIO.output(IN2, left_speed < 0)
    pwm_a.ChangeDutyCycle(abs(left_speed))
    # right motor
    GPIO.output(IN3, right_speed > 0)
    GPIO.output(IN4, right_speed < 0)
    pwm_b.ChangeDutyCycle(abs(right_speed))

def forward(speed=70):  set_motors(speed, speed)
def reverse(speed=70):  set_motors(-speed, -speed)
def turn_left(speed=60): set_motors(-speed, speed)
def turn_right(speed=60): set_motors(speed, -speed)
def stop():             set_motors(0, 0)

def cleanup():
    stop()
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()