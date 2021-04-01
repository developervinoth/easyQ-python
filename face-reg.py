# Start of Code
# Importing  required dependencies
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import requests

# Making a get request
url = 'https://hqueue-node.herokuapp.com/api/getBookings'

payload = {'date': "31-3-2021"}
response = requests.post(url, data=payload)

# print response
print(response)
# Specify the path of known images
path = r'D:\face-reg\images'


images = []
classNames = []


myList = os.listdir(path)

# getting image and name from the specified path
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# printing available names in the Faces Folder
print(classNames)

# Function to Encode the Known Faces


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Function to mark attendence in .csv(Excel Sheet)


encodeListKnown = findEncodings(images)

# Printing Acknowledgement after the encoding of known face is completed
print('Encoding Completed')

# Starting webcam
cap = cv2.VideoCapture(0)


while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        # Calling Markattendence function when the diffrence between Current Image and Previous Encodings
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            bookings = response.json()
            # print(bookings)
            # print("err")
            # print(bookings, "swdwsd")
            bookings1 = bookings["data"]["bookings"]
            for booking in bookings1:
                if(booking["Id"] == name):
                    print("true")
            updated = booking
            updated["patientVisited"] = True
            url = 'https://hqueue-node.herokuapp.com/api/userVisited'
            payload = updated
            response1 = requests.post(url, data=payload)
            # print(response1.json())

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)

# End of Code
