import requests
import json
import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, request, jsonify
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay
import asyncio
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np


app = Flask(__name__)
pcs = set()

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

class CameraStreamTrack(MediaStreamTrack):
    """
    A video stream track that streams video from the Raspberry Pi Camera.
    """
    kind = "video"

    def __init__(self):
        super().__init__()
        self.camera = PiCamera(resolution=(640, 480), framerate=24)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="bgr", use_video_port=True)
        self.frame = None
        self._relay = MediaRelay()

    async def recv(self):
        while True:
            for f in self.stream:
                frame = f.array
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.rawCapture.truncate(0)
                return self._relay.track(self).recv()


@app.route('/')
def index():
    """Serve the control page."""
    return render_template('control.ejs')  # Ensure you have this file set as .html or render correctly

@app.route('/offer', methods=['POST'])
async def on_offer():
    params = request.get_json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pc.addTrack(CameraStreamTrack())

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return jsonify({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')  # Make sure to use HTTPS in production
