import cv2
import mediapipe as mp

video=cv2.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands(max_num_hands=2,min_detection_confidence=0.7)
mpDraw=mp.solutions.drawing_utils

while True:
    flag, img = video.read()
    if(flag==False):
        break

    RGBimg=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detecthands=hands.process(RGBimg)

    if (detecthands.multi_hand_landmarks):
        for handLms in detecthands.multi_hand_landmarks:
            # This code runs once per hand
            h,w,c=img.shape
            fingertips=[4,8]
            points=[]
            for i in fingertips:
                lm=handLms.landmark[i]
                cx,cy=int(lm.x*w),int(lm.y*h)
                points.append((cx,cy))

                # used to add circle in finger tip
                cv2.circle(img,(cx,cy),15, (255,255,0),cv2.FILLED)

            for i in range(len(points)-1):
               cv2.line(img,points[i],points[i+1],(255,0,255),3)


            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

    cv2.imshow("Hand Landmarks",img)
    if(cv2.waitKey(1)==ord('q') or cv2.waitKey(1)==ord('Q') or cv2.waitKey(1)==27):
        break

video.release()
cv2.destroyAllWindows()
