import cv2
import mediapipe as mp

video=cv2.VideoCapture(0)

mpHands=mp.solutions.hands #Set up hand tracking
#solutions is a submodule within MediaPipe that includes all the pre-trained models for various tasks
#It contains all the functions, classes, and models that are related to hand tracking.

hands=mpHands.Hands(max_num_hands=2,min_detection_confidence=0.7) #Define how confident it should be

mpDraw=mp.solutions.drawing_utils #Enable you to draw hand landmarks on the video
#It includes functions to draw landmarks

while(True):
    flag,img=video.read()
    if(flag!=True):
        break

    RGBimg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #BGR image to RGB

    detecthands=hands.process(RGBimg) #tries to detect any hands present in that image
    #It returns an object that contains information about the detected hands(e.g landmarks, the number of hands detected)
    #The detection step (hands.process(RGBimg)) doesn't guarantee that hands will be detected in every frame
    #so it is necessary to check if the landmarks were detected before attempting to draw them


    #multi_hand_landmarks is a list that contains the landmarks of all detected hands in the image
    if(detecthands.multi_hand_landmarks): #checks whether any hand landmarks were detected

        #A single frame can have multiple hands in it so that's why we use loop here
        #but for single hand we can use
        #mpDraw.draw_landmarks(img,detecthands.multi_hand_landmarks[0],mpHands.HAND_CONNECTIONS)
        #but it would crash if no hand was detected or if you tried to use it with 2 hands later. So the loop is safer and more flexible

        for handLms in detecthands.multi_hand_landmarks: #each detected hand and lets us access and draw its landmarks
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)#draws the hand landmarks and the lines connecting them
            #passing the frame to draw on,the landmarks to draw at,and the connections to draw between

    cv2.imshow("Hand Landmarks",img)#actually a sequence of images

    if(cv2.waitKey(1)==ord('q') or cv2.waitKey(1)==ord('Q') or cv2.waitKey(1)==27): #Waits for 1 milliseconds for any key press.
        break

video.release()
cv2.destroyAllWindows()
