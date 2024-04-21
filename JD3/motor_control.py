import RPi.GPIO as GPIO
import websocket
import json

motorA_en = 17
motorA_forward = 27
motorA_backward = 22

motorB_en = 5
motorB_forward = 6
motorB_backward = 13

GPIO.setmode(GPIO.BCM)

GPIO.setup(motorA_en, GPIO.OUT)
GPIO.setup(motorA_forward, GPIO.OUT)
GPIO.setup(motorA_backward, GPIO.OUT)

GPIO.setup(motorB_en, GPIO.OUT)
GPIO.setup(motorB_forward, GPIO.OUT)
GPIO.setup(motorB_backward, GPIO.OUT)

pwm_A = GPIO.PWM(motorA_en, 1000)
pwm_B = GPIO.PWM(motorB_en, 1000)
pwm_A.start(0)
pwm_B.start(0)


def control_motor(motor, action, speed):
	if motor == 'A':
		enable = motorA_en
		forward = motorA_forward
		backward = motorA_backward
		pwm = pwm_A
	else:
		enable = motorB_en
		forward = motorB_forward
		backward = motorB_backward
		pwm = pwm_B

	pwm.ChangeDutyCycle(speed)

	if action == 'forward':
		GPIO.output(motorA_forward, True)
		GPIO.output(motorB_forward, True)
		GPIO.output(motorA_backward, False)
		GPIO.output(motorB_backward, False)
	elif action == 'backward':
		GPIO.output(motorA_forward, False)
		GPIO.output(motorB_forward, False)
		GPIO.output(motorA_backward, True)
		GPIO.output(motorB_backward, True)
	elif action == 'right':
		GPIO.output(motorA_forward, True)
		GPIO.output(motorB_forward, False)
		GPIO.output(motorA_backward, False)
		GPIO.output(motorB_backward, True)
	elif action == 'left':
		GPIO.output(motorA_forward, False)
		GPIO.output(motorB_forward, True)
		GPIO.output(motorA_backward, True)
		GPIO.output(motorB_backward, False)
	else:
		GPIO.output(motorA_forward, False)
		GPIO.output(motorB_forward, False)
		GPIO.output(motorA_backward, False)
		GPIO.output(motorB_backward, False)
		pwm_A.ChangeDutyCycle(0)
		pwm_B.ChangeDutyCycle(0)
	return

def on_message(ws, message):
	data = json.loads(message)
	motor = data['motor']
	action = data['action']
	speed = int(data['speed'])
	control_motor(motor, action, speed)

def on_error(ws, error):
	print(error)

def on_close(ws):
	print("### closed ###")
	GPIO.cleanup()
if __name__ == "__main__":
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("ws://10.0.2.15:3000",
	on_message = on_message, on_error = on_error, on_close = on_close)
	print(f"Message: {on_message}, Error: {on_error}, Close: {on_close}")
	ws.run_forever()
