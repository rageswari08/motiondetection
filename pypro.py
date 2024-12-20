import cv2
import imutils
import time

cam=cv2.VideoCapture(0)
time.sleep(1)

firstFrame=None
area=500


while  True:
    
    _,img=cam.read()
    text = "normal"

    img=imutils.resize(img,width=1000)

    grayImg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gaussianImg=cv2.GaussianBlur(grayImg,(21,21),0)

    if firstFrame is None:
      firstFrame = gaussianImg
      continue

    imgDiff =cv2.absdiff(firstFrame,gaussianImg)
    
    cv2.imshow("Frame Difference", imgDiff)

    threshimg=cv2.threshold(imgDiff,25,255,cv2.THRESH_BINARY)[1]
    threshimg=cv2.dilate(threshimg,None,iterations=2)
    cv2.imshow("Threshold", threshimg)
    cnts=cv2.findContours(threshimg.copy(),cv2.RETR_EXTERNAL,
                          cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)
    for c in cnts:
            if cv2.contourArea(c) < area:
               continue
            
            (x,y,w,h)=cv2.boundingRect(c)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            text="MOVING"
            
    print(text)


    cv2.putText(img,text,(10,20),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    cv2.imshow("camerafeed",img)

    key=cv2.waitKey(1) & 0xFF
    if key==ord("a"):
         break
    print("Exiting program. Closing camera...")

           
cam.release()
cv2.destroyAllWindows()
      
                          




