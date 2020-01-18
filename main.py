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
		start_time = time.time()
		while (time.time() - start_time) < 10:
			camera.wait_recording(2)
			camera.capture(image_stream, use_video_port=True, format='jpeg')
			# Spawn a separate thread for the request so video is not blocked
			Thread(target=make_request, args=(image_stream,)).start()
			camera.wait_recording(2)
		camera.stop_recording()


def get_request_params():
	request_params = {}
	request_params['headers'] = {'Ocp-Apim-Subscription-Key': '165fbaf18f434fd3a52fca8890ca2800', 'Content-type': 'application/octet-stream'}
	request_params['request_data'] = {'returnFaceAttributes':'emotion,smile', 'overload':'stream'}
	return request_params

def make_request(image_stream):
	print ("Making_request")
	lock_on_stream = lock.acquire()
	request_params = get_request_params()
	try:
		request_url = 'https://hackcambridge-emotiondetector.cognitiveservices.azure.com/face/v1.0/detect'
		request = requests.post(request_url, params=request_params['request_data'], headers=request_params['headers'], data=image_stream)
		print (request.json())
		image_stream.flush()
	finally:
		lock_on_stream = lock.release()

emotion_rec()
