from threading import Thread, Lock
import time
import cv2
import picamera
import requests
import io
from queue import *
from TextToSpeech import TextToSpeech

video_stream = io.BytesIO()
lock = Lock()
file_counter = 0

image_queue = LifoQueue(maxsize=100)
image_results = []
audio_generator = TextToSpeech('18cc0b753fa74192a6bac800febea621')
audio_generator.get_token()

def emotion_rec():
	image_stream = io.BytesIO()
	with picamera.PiCamera() as camera:
		camera.resolution = (640,480)
		camera.brightness = 60
		camera.rotation = 180
		camera.start_preview()
		time.sleep(2)
		camera.start_recording(video_stream, format='h264', quality=23)
		start_time = time.time()
		while (time.time() - start_time) < 20:
			camera.wait_recording(2)
			camera.capture(image_stream, use_video_port=True, format='jpeg')
			if image_queue.full():
				with image_queue.mutex:
					image_queue.clear()
			image_queue.put(image_stream)
			image_stream = io.BytesIO()
			Thread(target=make_request).start()
		camera.stop_recording()
		camera.stop_preview()


def get_request_params():
	request_params = {'headers': {'Ocp-Apim-Subscription-Key': '165fbaf18f434fd3a52fca8890ca2800',
								  'Content-type': 'application/octet-stream'},
					  'request_data': {'returnFaceAttributes': 'emotion,smile', 'overload': 'stream'}}
	return request_params

def make_request():
	#global file_counter
	request_params = get_request_params()
	previous_prominent_emotion = ""
	while not image_queue.empty():
		# print (image_queue.size())
		image_to_request = image_queue.get()
		try:
			#with open("test_file_{0}.jpeg".format(file_counter), "wb") as fp:
				#image_to_request.seek(0)
				#file = image_to_request.read()
				#fp.write(file)
				#file_counter+=1
			image_to_request.seek(0)
			request_url = 'https://hackcambridge-emotiondetector.cognitiveservices.azure.com/face/v1.0/detect'
			request = requests.post(request_url, params=request_params['request_data'], headers=request_params['headers'], data=image_to_request)
			print (request.json())
			prominent_emotion = find_prominent_emotion(request.json()) if len(request.json()) > 0 else ""
			# This is only triggered on a change of emotion
			if previous_prominent_emotion != prominent_emotion and len(request.json()) > 0 and prominent_emotion != "":
				previous_prominent_emotion = prominent_emotion
				audio_generator.save_audio(prominent_emotion)
				time.sleep(2)
		except Exception as e:
			print (e)

def find_prominent_emotion(emotion_dictionary):
	print ("Finding prominent emotions")
	detectable_emotions = emotion_dictionary[0]['faceAttributes']['emotion']
	sorted_emotions = [k for k, v in sorted(detectable_emotions.items(), key=lambda item: item[1])]
	print ("Sorted", sorted_emotions)
	return sorted_emotions[-1]
emotion_rec()
