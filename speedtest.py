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

def getport():
  ports=list(serial.tools.list_ports.comports())
  return ports[0].device

cascade=cv.CascadeClassifier('cascade-2.xml')
ardu=serial.Serial(port=getport(),baudrate=115200,timeout=1)


if __name__ == "__main__":
  cam=cv.VideoCapture(0)

  cam.set(cv.CAP_PROP_FRAME_WIDTH, sx)
  cam.set(cv.CAP_PROP_FRAME_HEIGHT, sy)
  mx=0
  my=0

  while(True):
    ret,frame=cam.read()

    frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    frame=cv.resize(frame,(dx,dy))

    signs=cascade.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=7)
    for(x,y,w,h) in signs:
      mx=x+w/2
      my=y+h/2
      #box the sign
      cv.rectangle(frame,(x,y),(x+w,y+h),color=(0,0,255),thickness=3)
      #print(x," ",y)
    cv.imshow('img',frame)


    ardu.write(bytes([201]))
    ardu.write(bytes([200]))
    time.sleep(0.05)
    if(signs==()):
      ardu.write(bytes([214]))
      print('nothing detected')      
    else:
      print(mx," ",my)
      if (mx>(2/3*dx)):
        #ardu.write(bytes([212]))
        print('right')
      elif (mx<(1/3*dx)):
        #ardu.write(bytes([213]))
        print('left')
      elif (mx>(1/3*dx) and mx<(2/3*dx)):
        ardu.write(bytes([210]))
        print('forward')
      else:
        #ardu.write(bytes([225]))
        print('if this shows up you made a mistake')

