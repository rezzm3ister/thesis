import cv2 as cv
import time
import numpy as np
import serial
import serial.tools.list_ports

#main cam res size
sx=1280
sy=720

#sign detection size, defaults 640x360
dx=640
dy=360

#depth detect size, we dont need any bigger than 144p.
#vx=256
#vy=144

cascade=cv.CascadeClassifier('cascade-2.xml')

if __name__ == "__main__":
  cam=cv.VideoCapture(0)

  cam.set(cv.CAP_PROP_FRAME_WIDTH, sx)
  cam.set(cv.CAP_PROP_FRAME_HEIGHT, sy)
  mx=0
  my=0

  i=0
  falses=0
  while(True):
    ret,frame=cam.read()

    frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    frame=cv.resize(frame,(dx,dy))

    if cv.waitKey(1) & 0xFF == ord('q'):
      break

    if i>500:
      #false
      #print("in ",i," frames, detected ",falses," false positives")
      #positive
      print("in ",i-1," frames, detected ",falses," frames with a marker")
      print("detect rate: ",falses/(i-1))

      break

    signs=cascade.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=10)
    frame=cv.cvtColor(frame,cv.COLOR_GRAY2BGR)
    for(x,y,w,h) in signs:
      #counts false hits
      #falses+=1

      mx=x+w/2
      my=y+h/2
      #box the sign
      cv.rectangle(frame,(x,y),(x+w,y+h),color=(0,0,255),thickness=3)
      #print(x," ",y)
    
    cv.imshow('img',frame)
    print("frame: ",i)
    if(signs==()):
      #ardu.write(bytes(['s']))
      print('nothing detected')      
    else:
      #detections
      falses+=1
      print(mx," ",my)
      print("markers detected: ",signs.size/4)
      if (mx>(2/3*dx)):
        #ardu.write(bytes([212]))
        print('right')
      elif (mx<(1/3*dx)):
        #ardu.write(bytes([213]))
        print('left')
      elif (mx>(1/3*dx) and mx<(2/3*dx)):
        #ardu.write(bytes([210]))
        print('forward')
      else:
        #ardu.write(bytes([225]))
        print('if this shows up you made a mistake')
    i+=1
  cv.destroyAllWindows()

