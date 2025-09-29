import cv2
import mediapipe as mp
import time

video = cv2.VideoCapture(0)

mpHands = mp.solutions.hands  
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)  
mpDraw = mp.solutions.drawing_utils  

#for calculating fps
pTime=0 #previous time
cTime=0 #current time

while True:
    flag,img=video.read()
    if(flag==False):
        break
        
    RGBimg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  
    result=hands.process(RGBimg)
    
    if(result.multi_hand_landmarks):

        for handLms in result.multi_hand_landmarks:
            h,w,c=img.shape
            fingertips=[4,8]
            points=[]
            for i in fingertips:
                lm=handLms.landmark[i]
                cx,cy=int(lm.x*w),int(lm.y*h)
                points.append((cx, cy))

                cv2.circle(img,(cx, cy),15,(255, 255, 0),cv2.FILLED)

            for i in range(len(points)-1):
                cv2.line(img,points[i],points[i+1],(255,0,255),3)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if(cv2.waitKey(1)==ord('q') or cv2.waitKey(1)==ord('Q') or cv2.waitKey(1)==27):
        break

    cTime=time.time()#gets the current time in seconds as a floating-point number.
    fps=1/(cTime-pTime)#calculates how much time passed since the last frame
    pTime=cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)#pecifically the calculated FPS value.
    #only accepts text as a string, not an int or float.
    cv2.imshow("Hand Landmarks",img)

video.release()
cv2.destroyAllWindows()
