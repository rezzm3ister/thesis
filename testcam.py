import cv2 as cv


vid=cv.VideoCapture(1)

while(True):
    ret,frame=vid.read()
    #frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        
    #cv.imshow('img',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
      break
    

    cv.imshow('img',frame)