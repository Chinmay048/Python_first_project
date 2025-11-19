import cv2
import mediapipe as mp

video=cv2.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands(max_num_hands=2,min_detection_confidence=0.7)
mpDraw=mp.solutions.drawing_utils

while(True):
    flag,img=video.read()
    if(flag==False):
        break

    RGBimg=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    detecthands=hands.process(RGBimg)

    if (detecthands.multi_hand_landmarks):  
        for handLms in detecthands.multi_hand_landmarks:  

            #This code runs once per hand
            h,w,c=img.shape #Get image dimensions-height,width,channel
            fingertips=[4,8]# Get coordinates of finger tips
            points=[]
            for i in fingertips:
                lm=handLms.landmark[i] #gives the landmark object.
                cx,cy=int(lm.x*w),int(lm.y*h) #converts normalized landmark coordinates from MediaPipe into pixel coordinates on your image.
                points.append((cx,cy))# storing the pixel coordinates of each fingertip

            #we can use
            #for i in range(1):  #when we connect only 2 tips that is of a hand

            for i in range(len(points)-1):
                cv2.line(img,points[i],points[i+1],(255,0,255),3)# saves the position of that fingertip into the list

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)  # draws the hand landmarks and the lines connecting them

    cv2.imshow("Hand Landmarks", img)
    if(cv2.waitKey(1)==ord('q') or cv2.waitKey(1)==ord('Q') or cv2.waitKey(1)==27):
        break

video.release()
cv2.destroyAllWindows()
