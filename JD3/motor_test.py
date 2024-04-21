import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

IN1 = 22
IN2 = 27

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)


def motor_forward():
	GPIO.output(IN1, GPIO.HIGH)
	GPIO.output(IN2, GPIO.LOW)

def motor_stop():
	GPIO.output(IN1, GPIO.LOW)
	GPIO.output(IN2, GPIO.LOW)

motor_forward()
time.sleep(5)
motor_stop()
GPIO.cleanup()
