import cv2

video=cv2.VideoCapture(0) #opens webcam

while(True):
    flag,img=video.read() #return two values, True if successfully captured and image

    if(flag!=True):
        break


    cv2.imshow("Video",img)#actually a sequence of images

    if (cv2.waitKey(1)==ord('q') or cv2.waitKey(1)==ord('Q') or cv2.waitKey(1)==27):
        break

video.release() #used so that other apps can used webcam
cv2.destroyAllWindows()
