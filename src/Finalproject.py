import cv2
import mediapipe as mp
import time
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

#Initialize webcam
video = cv2.VideoCapture(0)

#Initialize mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Setup pycaw to control system volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

#Initializing FPS
pTime=0
cTime=0

while True:
    flag, img = video.read()
    if(flag==False):
        break

    RGBimg=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detecthands=hands.process(RGBimg)

    if (detecthands.multi_hand_landmarks):
        for handLms in detecthands.multi_hand_landmarks:
            h,w,c=img.shape
            fingertips=[4,8]
            points=[]
            for i in fingertips:
                lm=handLms.landmark[i]
                cx,cy=int(lm.x*w),int(lm.y*h)
                points.append((cx,cy))
                cv2.circle(img,(cx,cy),15,(255,255,0),cv2.FILLED)

            x1,y1=points[0]
            x2,y2=points[1]
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            distance=math.hypot(x2-x1,y2-y1)
            max_distance=250
            percentage=(min(distance,max_distance)*100)//max_distance

            cv2.putText(img, f'{int(percentage)}%', (10, 120), cv2.FONT_ITALIC, 1, (0, 255,0), 2)


            volume_level = volMin + (percentage / 100) * (volMax - volMin)
            volume.SetMasterVolumeLevel(volume_level, None)  # Set the system volume


            x_start = 50
            y_start = 400
            bar_height = 250
            bar_width = 20
            bar_fill = int(min(distance, bar_height))
            cv2.rectangle(img, (x_start,y_start - bar_height), (x_start + bar_width, y_start), (200, 200, 200), 2)
            cv2.rectangle(img, (x_start,y_start - bar_fill), (x_start + bar_width, y_start),(0, 255, 0),cv2.FILLED)

            for i in range(len(points)-1):
                cv2.line(img,points[i],points[i+1],(0,0, 255),3)

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)


    key=cv2.waitKey(1)
    if (key==ord('q') or key==ord('Q') or key==27):
        break

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(10, 70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),3)

    cv2.imshow("Hand Landmarks", img)

video.release()
cv2.destroyAllWindows()

