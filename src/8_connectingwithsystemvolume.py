import cv2
import mediapipe as mp
import time
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#pycaw is a package
#Provides functions to access audio devices and audio sessions on your Windows system
from ctypes import cast, POINTER
#A Python file (written in C internally) that comes with Python
#convert (or "cast") a pointer or address in memory into A specific class, structure, or COM interface that the memory is actually pointing
#creates a pointer type for a given ctypes-compatible type
from comtypes import CLSCTX_ALL
#comtypes is a package.
#Python library that provides bindings to COM (Component Object Model) interfaces.
#CLSCTX_ALL is a constant defined in the comtypes module.It is used to specify the context or environment in which a COM object should be instantiated.



video = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Setup pycaw to control system volume
devices = AudioUtilities.GetSpeakers() #retrieves the default audio output device on the system
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#this line is activating the volume control interface for the speakers device, enabling you to interact with the audio volume programmatically
#IAudioEndpointVolume._iid_ parameter specifies the Interface Identifier (IID), which controls the volume of the audio device
#CLSCTX_ALL tells the system to activate the COM object
volume = cast(interface, POINTER(IAudioEndpointVolume))
#cast() function is used to convert the interface object into a pointer to the
#POINTER(IAudioEndpointVolume) tells pycaw that the object is a pointer to the IAudioEndpointVolume interface, which allows you to access different methods

# Get volume range (min, max)
volMin, volMax = volume.GetVolumeRange()[:2]  # usually something like -65.25(Min) to 0.0(Max),only care about the min and max, not the step
#This method gets the volume range of the audio device

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

            # Map the distance to the system volume range
            # Convert the hand distance percentage to a volume level
            volume_level = volMin + (percentage / 100) * (volMax - volMin)
            #percentage / 100 -This converts the percentage into a value between 0 and 1.
            #(volMax - volMin)-This gives the total span between the minimum and maximum volume levels
            #(percentage / 100) * (volMax - volMin): This calculates how far along the range the volume should be based on the percentage
            #Finally, adding volMin shifts this result into the actual range of system volume

            volume.SetMasterVolumeLevel(volume_level, None)  # Set the system volume


            x_start = 50
            y_start = 400
            bar_height = 250
            bar_width = 20
            bar_fill = int(min(distance, bar_height))
            cv2.rectangle(img, (x_start,y_start - bar_height), (x_start + bar_width, y_start), (200, 200, 200), 2)
            cv2.rectangle(img, (x_start,y_start - bar_fill), (x_start + bar_width, y_start),(0, 255, 0),cv2.FILLED)

            for i in range(len(points)-1):
                cv2.line(img,points[i],points[i+1],(255,0, 255),3)

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

    #We need to press multiple times q/Q/Esc button for stop execution because we are calling cv2.waitKey(1) multiple times in the loop
    #if(cv2.waitKey(1)==ord('q') or cv2.waitKey(1)==ord('Q') or cv2.waitKey(1)==27):

    key=cv2.waitKey(1)
    if (key==ord('q') or key==ord('Q') or key==27 ):
        break

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(10, 70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),3)

    cv2.imshow("Hand Landmarks", img)

video.release()
cv2.destroyAllWindows()
