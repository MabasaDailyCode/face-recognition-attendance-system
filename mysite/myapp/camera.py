import os
import face_recognition
import cv2
import numpy as np
from datetime import datetime, date
from datetimerange import DateTimeRange

path = os.getcwd()
print(path)
print(os.listdir())
from imutils import paths

file_name = "Attendance database"
paths = os.listdir(file_name)
print(paths)
print("Load faces .....")
faces = []
faces_label = []
for name in os.listdir(file_name):
    for filename in os.listdir(f'{file_name}/{name}'):
        image = face_recognition.load_image_file(f'{file_name}/{name}/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        if len(encoding) > 0:
            faces.append(encoding)
            faces_label.append(name)
face_locations = []
face_encodings = []
face_names = []

def attendance(name):
    # Opening the CSV file
    with open("attendance.csv", 'r+') as f:
        mylist = f.readlines()
        namelist = []
        print(mylist)
        for line in mylist:
            entry = line.split(',')
            namelist.append(entry[0])
        # insert records that haven't yet been recorded
        if name not in namelist:
            dat = date.today()
            now = datetime.now()
            dt = now.strftime('%H:%M:%S')
            # Optional, you can specify the time range
            time_range = DateTimeRange("06:30:30", "08:30:30")
            if dt in time_range:
                status = 'Present'
            else:
                status = 'Late'
            f.writelines(f'\n{name},{dat},{status},{dt}')

class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    def __del__(self):
        self.cap.release()
    def get_frame(self):
        process_this_frame = True
        ret, frame = self.cap.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(faces, face_encoding)
                name = "Unknown"
                # use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(faces, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = faces_label[best_match_index]
                # If an unregistered face is detected, an "Unknown" label is assigned to it.
                face_names.append(name)
        process_this_frame = not process_this_frame
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, str(name), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # All faces labeled "Unknown" will not be entered in the attendance file
            if name != 'Unknown':
                attendance(name)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
