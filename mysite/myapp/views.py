from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
import os
import cv2
import posixpath
import time

def index(request):
    return render(request, "Welcome.html")
def home(request):
    return render(request, "Pictures.html")

def register(request):
    return render(request, "home.html")

def take_attendance(request):
    return render(request, "Menu.html")

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_cap(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def home_view(request):
    # Get file name from the registration interface
    dir_name = request.GET.get('your_name')
    path = os.getcwd()
    file_name = "Attendance database"
    new_path = os.path.join(path, file_name)
    print(new_path)
    # Creating a folder in the database by joining the paths together with the file name from the interface
    p = os.path.join(new_path, dir_name)
    os.mkdir(p)
    check_file = os.path.exists(p)
    if check_file == True:
        newPath = os.path.join(new_path, p)
        print(newPath)
        # Capture 10 images from a video feed and save them in the created directory
        camera = cv2.VideoCapture(0)
        time.sleep(10)
        for i in range(10):
            return_value, image = camera.read()
            v = os.path.join(newPath, dir_name)
            cv2.imwrite(v + str(i) + '.jpg', image)
        del(camera)
    return render(request, "home.html")
