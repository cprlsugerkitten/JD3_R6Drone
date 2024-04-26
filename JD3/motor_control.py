import RPi.GPIO as GPIO
import websocket
import json
import time

#motorA_en = 17
motorA_forward = 22
motorA_backward = 27

#motorB_en = 5
motorB_forward = 6
motorB_backward = 13

GPIO.setmode(GPIO.BCM)

#GPIO.setup(motorA_en, GPIO.OUT)
GPIO.setup(motorA_forward, GPIO.OUT)
GPIO.setup(motorA_backward, GPIO.OUT)

#GPIO.setup(motorB_en, GPIO.OUT)
GPIO.setup(motorB_forward, GPIO.OUT)
GPIO.setup(motorB_backward, GPIO.OUT)

# pwm_A = GPIO.PWM(motorA_en, 1000)
# pwm_B = GPIO.PWM(motorB_en, 1000)
# pwm_A.start(0)
# pwm_B.start(0)


def control_motor(motor, action, speed):
	if motor == 'A':
		#enable = motorA_en
		forward = motorA_forward
		backward = motorA_backward
		#pwm = pwm_A
	else:
		#enable = motorB_en
		forward = motorB_forward
		backward = motorB_backward
		#pwm = pwm_B

	#pwm.ChangeDutyCycle(speed)

	if action == 'forward':
		GPIO.output(motorA_forward, GPIO.HIGH)
		GPIO.output(motorB_forward, GPIO.HIGH)
		GPIO.output(motorA_backward, GPIO.LOW)
		GPIO.output(motorB_backward, GPIO.LOW)
	elif action == 'backward':
		GPIO.output(motorA_forward, GPIO.LOW)
		GPIO.output(motorB_forward, GPIO.LOW)
		GPIO.output(motorA_backward, GPIO.HIGH)
		GPIO.output(motorB_backward, GPIO.HIGH)
	elif action == 'right':
		GPIO.output(motorA_forward, GPIO.HIGH)
		GPIO.output(motorB_forward, GPIO.LOW)
		GPIO.output(motorA_backward, GPIO.LOW)
		GPIO.output(motorB_backward, GPIO.HIGH)
	elif action == 'left':
		GPIO.output(motorA_forward, GPIO.LOW)
		GPIO.output(motorB_forward, GPIO.HIGH)
		GPIO.output(motorA_backward, GPIO.HIGH)
		GPIO.output(motorB_backward, GPIO.LOW)
	elif action == 'stop':
		GPIO.output(motorA_forward, GPIO.LOW)
		GPIO.output(motorB_forward, GPIO.LOW)
		GPIO.output(motorA_backward, GPIO.LOW)
		GPIO.output(motorB_backward, GPIO.LOW)
		#pwm_A.ChangeDutyCycle(0)
		#pwm_B.ChangeDutyCycle(0)
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
	#control_motor('A', 'forward', 50)
	time.sleep(5)
	#control_motor('A', 'stop', 50)
	ws = websocket.WebSocketApp("ws://172.20.10.4:8080",
	on_message = on_message, on_error = on_error, on_close = on_close)
	print(f"Message: {on_message}, Error: {on_error}, Close: {on_close}")
	ws.run_forever()
# if __name__ == "__main__":
	# with connect("ws://172.20.10.4:8080") as websocket:
		# message = websocket.recv()
		
