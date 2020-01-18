# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


class Camera:

    def __init__(self, size, framerate):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = size
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(camera, size=size)

    def get_capture_frame_iterator(self, f="bgr", video_port=True):
         return camera.capture_continuous(self.rawCapture, format=f, use_video_port=video_port)

    def truncate(self):
        self.rawCapture.truncate(0)


if __name__ == "__main__":
    cam = Camera((640, 480), 32)

    time.sleep(0.1) # let the camera initialise

    for frame in cam.get_capture_frame_iterator():
        image = frame.array

        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        cam.truncate()

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
