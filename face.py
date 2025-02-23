import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import requests

# Path to the directory containing the images
path = "D:/Test Images"
images = []
classNames = []
MyList = os.listdir(path)
print(MyList)

# Load images and extract class names
for cl in MyList:
    curIm = cv2.imread(f'{path}/{cl}')
    images.append(curIm)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

# Function to find encodings of the images
def findEncodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

# Encode known images
encodeListKnown = findEncodings(images)
print("Encoding Complete")

# Function to mark attendance by sending a POST request to the Flask server
def markAttendance(name):
    url = 'http://127.0.0.1:5000/mark_attendance'
    response = requests.post(url, data={'name': name})
    if response.status_code == 409:
        print(f"{name} - Attendance already marked")

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break
    
    # Resize and convert the frame
    imgs = cv2.resize(img, None, fx=0.25, fy=0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    # Find face locations and encodings in the current frame
    faceCurrFrame = face_recognition.face_locations(imgs)
    encofaceCurr = face_recognition.face_encodings(imgs, faceCurrFrame)

    for encodeFace, faceloc in zip(encofaceCurr, faceCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        facedis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(facedis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

    cv2.imshow("Face Recognition", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
