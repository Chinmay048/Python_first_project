import cv2
import mediapipe as mp
import time
import math

video = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

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

            #Calculating distance between two points
            #assigning the pixel coordinates of two fingertips
            x1,y1=points[0]
            x2,y2=points[1]
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            distance=math.hypot(x2-x1,y2-y1)

            #showing distance
            cv2.putText(img, f'Distance:{int(distance)}', (10, 100), cv2.FONT_ITALIC, 1, (0, 255,), 2)

            for i in range(len(points)-1):
                cv2.line(img,points[i],points[i+1],(255,0, 255),3)

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

    if(cv2.waitKey(1)==ord('q') or cv2.waitKey(1)==ord('Q') or cv2.waitKey(1)==27):
        break

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(10, 70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),3)

    cv2.imshow("Hand Landmarks", img)

video.release()
cv2.destroyAllWindows()
