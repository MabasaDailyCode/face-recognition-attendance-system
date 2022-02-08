
# Realtime web-based automated multiple face recognition attendance system using django.

The main objective of this project is to develop a web-based automated multiple student face recognition attendance system using the deep learning library face recognition. To check the attendance, student faces are captured from a real-time video stream and employs deep learning neural networks to check whether the detected student face matches anyone in the database, and (if yes) further identifies the name of the student. The output results of the face recognition will be used to update the attendance record in the format of an excel file.


## Screenshots

- ![App Screenshot2](https://via.placeholder.com/468x300?text=App+Screenshot+Heres)


# Installation
## Requirements

- python 3.6 or older version which supports dlib
- Django 3.2
- C++ environment is required in order to install CMake successfully thus install Microsoft visual studio 2015 rather than 2017 first. Check https://visualstudio.microsoft.com/vs/older-downloads/#visual-studio-2015-and-other-products

## Setup

1. Install CMake 

- Download CMake file from the following link: https://cmake.org/download/
- *Note:* During the installation, click “Add CMake to system path”.
 ```pip
   # Check if it was installed successfully 
   cmake --version
```

2. Install dlib   

 ```pip
   pip install dlib
```

3. Install face recognition library
```pip
  pip install face_recognition
```
- for more info check:- https://github.com/ageitgey/face_recognition#installation
4. Install Django
```pip
  pip install Django
```
- For more info, refer to the Django website https://www.djangoproject.com/download/
- Video Tutorial: https://youtu.be/FNQxxpM1yOs
## Usage/Examples
### Registration 

**1. Manual**
- The manual registration method is currently the most effective way for registration. You just create a folder labeled the student’s name and manually insert the images. Once the folder has been inserted in the record database, the new student’s faces are able to be recognized in the video feed during taking attendance.

**2. Using the interface**
- The user can access the website and navigate to the registration button to register new students. To register new students, the user enters the name of the student into the textbox of the form and click “OK”. Once its submitted the form id and input text (name) are displayed in the url which will be taken by the request.Get() function to the code. The function will get the name used to register a student then use it to execute the code for making a directory in which the image data will be saved. Once the “OK” button is clicked the camera captures faces from the video frames once the program is executed. However, since the camera takes less than 10 seconds once it opens to capture the images, it is impossible to have a visual of the video feed hence the user before clicking "OK" they have to position the person on the right camera position. Once the camera turns off, the captured images will already have been taken and saved directly into the student database file/folder created. Then the system requires the user 
**Creating directory and capture images code in views.py**

```python
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
```
**Open camera and detect faces**

```python
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
```
**Mark attendance**

```python
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
            # Optional, you can specify the time range of your choice
            time_range = DateTimeRange("06:30:30", "08:30:30")
            if dt in time_range:
                status = 'Present'
            else:
                status = 'Late'
            f.writelines(f'\n{name},{dat},{status},{dt}')
```

## Running Tests

To run application, run the following command:

```python
  python manage.py runserver
```

- After executing the above command, to access the application enter http://127.0.0.1:8000/webapp/ 

To access the registration, directly use this link since the registration button currently has a problem yet to be fixed.
-  http://127.0.0.1:8000/webapp/home_view?your_name=myfolder
**Note:** The manual method is currently the most effective way to register new users.
## Feedback

If you have any feedback, please reach out to me at nyasha@163.com

