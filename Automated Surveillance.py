import time
import cv2
import datetime
from playsound import playsound
from datetime import datetime
from threading import Thread

def alert():
    playsound('alert.mp3', False)

def Processing(file, file_save):
    if file == '0':
        file = int(file)

    cap = cv2.VideoCapture(0)

    ret, frame1 = cap.read()
    height, width, _ = frame1.shape
    ret, frame2 = cap.read()

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    Output = cv2.VideoWriter(file_save, fourcc, 20.0, (width, height))
    recording_time = datetime.now().strftime('%Y-%b-%d-%H-%S-%f')
    Output2 = cv2.VideoWriter('Movements/Video ' + str(recording_time) + '.avi', fourcc, 30.0, (width, height))


    while cap.isOpened():

        Output.write(frame1)
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        datex = str(datetime.now())
        font = cv2.FONT_HERSHEY_TRIPLEX
        cv2.putText(frame1, datex, (10, 20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


        if contours == ( ):
            cv2.putText(frame1, "STATUS : STATIONARY", (480, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        else:

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) < 1000:

                    continue

                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame1, "STATUS : MOVEMENT", (480, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                Output2.write(frame1)




        cv2.imshow('FEED', frame1)
        B = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        L = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(40) == 27:
            break

    cv2.destroyAllWindows()

File = "Cam_Detection.mp4"  # input('\nEnter location of video: ')
File_Save = "Recording/VideoRecording"+str(datetime.now().strftime('%Y-%b-%d-%H-%S-%f'))+".avi"  # input('\nEnter the location to save video: ')

Processing(File, File_Save)