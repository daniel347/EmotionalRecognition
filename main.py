from threading import Thread, Lock
import time
import cv2
import picamera
import requests
import io

def emotion_rec():
	stream = io.BytesIO()
	with picamera.PiCamera() as camera:
		camera.resolution = (640,480)
		camera.start_recording(stream, format='h264', quality=23)
		camera.wait_recording(5)
		camera.stop_recording()
	request_url = 'https://hackcambridge-emotiondetector.cognitiveservices.azure.com/face/v1.0/detect?overload=stream&returnFaceAttributes=["smile", "emotion]'
	print (stream)
	request = requests.post(request_url, data=stream)
	print (request.json())	

emotion_rec()
