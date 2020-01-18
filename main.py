from threading import Thread, Lock
import time
import cv2
import picamera
import requests
import io

video_stream = io.BytesIO()
image_stream = io.BytesIO()
lock = Lock()

def emotion_rec():
	with picamera.PiCamera() as camera:
		camera.resolution = (640,480)
		camera.start_recording(video_stream, format='h264', quality=23)
		start_time = 
		while :
			camera.wait_recording(2)
			camera.capture(image_stream, use_video_port=True)
			# Spawn a separate thread for the request so video is not blocked
			Thread(target=make_request, args=(image_stream,))
			camera.wait_recording(2)
			camera.stop_recording()

def make_request(image_stream):
	lock
	request_url = 'https://hackcambridge-emotiondetector.cognitiveservices.azure.com/face/v1.0/detect?overload=stream'
	headers = {'apiKey':'165fbaf18f434fd3a52fca8890ca2800'}
	request = requests.post(request_url, headers=headers, data=stream)
	print (request.json())	

emotion_rec()
