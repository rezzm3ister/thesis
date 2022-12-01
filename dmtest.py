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
vx=320
vy=180

if __name__ == "__main__":
  left=cv.VideoCapture(0)
  right=cv.VideoCapture(1)
  left.set(cv.CAP_PROP_FRAME_WIDTH, sx)
  left.set(cv.CAP_PROP_FRAME_HEIGHT, sy)
  right.set(cv.CAP_PROP_FRAME_WIDTH, sx)
  right.set(cv.CAP_PROP_FRAME_HEIGHT, sy)
 

  i=0
  falses=0
  while(True):
    retl,fl=left.read()
    retr,fr=right.read()

    fl=cv.cvtColor(fl,cv.COLOR_BGR2GRAY)
    fr=cv.cvtColor(fr,cv.COLOR_BGR2GRAY)

    #frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    if cv.waitKey(1) & 0xFF == ord('q'):
      break

    dfl=cv.resize(fl,(vx,vy))
    dfr=cv.resize(fr,(vx,vy))
    stereo=cv.cuda.StereoSGM.create(minDisparity=10,numDisparities=24,blockSize=6)
    depth=stereo.compute(dfl,dfr)
    cv.imshow("L",dfl)
    cv.imshow("R",dfr)
    cv.imshow("depth",depth/1280)

    centerdepth=depth[(vy//3):(vy//3*2),(vx//3):(vx//3*2)]
    cv.imshow("cdepth",centerdepth/1000)
    centerdist=np.mean(centerdepth) #add some kind of multiplier
    
    #change second array with actual measurement
    #centerdistmm=np.interp(centerdist,[300,250],[100,2000])

    #send speed
    speed=int(np.interp(centerdist,[200,400],[200,0]))

    print("speed (/200): ",speed)
  cv.destroyAllWindows()
