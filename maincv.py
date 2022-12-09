#alvarez angeles thesis

#THIS CODE REQUIRES OPENCV-CUDA TO BE INSTALLED
#IT ALSO REQUIRES 2 WEBCAMS


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

#get arduino port
#theres only one serial device anyway so it just gets the first one.
def getport():
  ports=list(serial.tools.list_ports.comports())
  return ports[0].device



#ARDUINO CONNECT, UNCOMMENT LINE BELOW FOR ARDUINO
ardu=serial.Serial(port=getport(),baudrate=115200,timeout=1)

if __name__ == "__main__":
  #initialize both cameras
  left=cv.VideoCapture(0)
  right=cv.VideoCapture(1)
  left.set(cv.CAP_PROP_FRAME_WIDTH, sx)
  left.set(cv.CAP_PROP_FRAME_HEIGHT, sy)
  right.set(cv.CAP_PROP_FRAME_WIDTH, sx)
  right.set(cv.CAP_PROP_FRAME_HEIGHT, sy)
  #set up cuda Mats
  gl=cv.cuda_GpuMat()
  gr=cv.cuda_GpuMat()
  gd=cv.cuda_GpuMat()
  font = cv.FONT_HERSHEY_SIMPLEX

  #frametime fps counter params
  ft=0
  pft=0

  #setting cascade
  cascade=cv.CascadeClassifier('cascade-2.xml')
  cudacascade=cv.cuda_CascadeClassifier.create('cascade-2.xml')
  mx=0
  my=0
  #this probably isnt used
  tempgpu=cv.cuda_GpuMat()
  
  cv.namedWindow('img')
  while(True):
    #get both cam views
    if cv.waitKey(1) & 0xFF == ord('q'):
      break

    retl,fl=left.read()
    retr,fr=right.read()

    #make grayscale for better performance
    fl=cv.cvtColor(fl,cv.COLOR_BGR2GRAY)
    fr=cv.cvtColor(fr,cv.COLOR_BGR2GRAY)

    #sign detection section
    #using LEFT eye
    DMSframe=cv.resize(fl,(dx,dy))
    #gframe=tempgpu.upload(DMSframe)

    #cascade detector, fiddle with this
    #default minneighbors =7
    signs=cascade.detectMultiScale(DMSframe,scaleFactor=1.1,minNeighbors=7)

    #cuda cascade doesnt work weirdly
    #signs=cudacascade.detectMultiScale(DMSframe)


    #allow color again for boxing    
    DMSframe=cv.cvtColor(DMSframe,cv.COLOR_GRAY2BGR)
    for(x,y,w,h) in signs:
      mx=x+w/2
      my=y+h/2
      #box the sign
      cv.rectangle(DMSframe,(x,y),(x+w,y+h),color=(0,0,255),thickness=3)
      #print(x," ",y)
    cv.imshow('img',DMSframe)


    #DEPTH MAP, this uses gpu
    dfl=cv.resize(fl,(vx,vy))
    dfr=cv.resize(fr,(vx,vy))
    stereo=cv.cuda.StereoSGM.create(minDisparity=10,numDisparities=24,blockSize=4,speckleRange=4)
    depth=stereo.compute(dfl,dfr)
    cv.imshow("depth",depth/1280)

    centerdepth=depth[(vy//3):(vy//3*2),(vx//3):(vx//3*2)]
    cv.imshow("cdepth",centerdepth/1280)
    centerdist=np.mean(centerdepth) #add some kind of multiplier
    
    #change second array with actual measurement
    #centerdistmm=np.interp(centerdist,[300,250],[100,2000])

    #send speed
    speed=int(np.interp(centerdist,[200,450],[200,0]))


    #depth regions NOT NEEDED ANYMORE
    #dmat=np.zeros((8,8))
    #dmx=vx//8
    #dmy=vy//8

    #refer to function above
    #dmat=getdispsum(depth)
    #nearcount=(dmat>175000).sum()

    #count number of pixels above a certain disparity threshold
    #number before stopping TBD
    #default: 350,600 at 144p
    nearcount=(depth>485).sum()

    verynearcount=(depth>700).sum()

  
    #debugging prints
    #print(dmat)
    print("points above threshold: ",nearcount," ",verynearcount)
    print(" ")
    #print(depth)
    #print(ardu)
    
    #FPS COUNTER
    ft=time.time()
    fps=1/(ft-pft)
    #cv.putText(depth, str(fps), (7, 70), font, 1, 255, 3, cv.LINE_AA)
    print("fps: ",fps)
    print("speed: ",centerdist," ",speed)
    pft=ft


    
    #SEND DATA TO ARDUINO
    #uncomment after
    ardu.write(bytes([201]))
    ardu.write(bytes([speed]))
    time.sleep(0.05)
    
    if(signs==()):
      #ardu.write(bytes(['s']))
      #default 144p 7000
      if(nearcount>7000):
        ardu.write(bytes([211]))
        print('b')
      else:
        ardu.write(bytes([214]))
        print('s')

      
    else:
      print(mx," ",my)
      #default 144p 2000,5000
      #speed=200
      
      if(nearcount>3000):
        if(nearcount>9000):
          print('b')
          ardu.write(bytes([211]))
        else:
          print('s')
          ardu.write(bytes([214]))
      else:
        if (mx>(2/3*dx)):
          ardu.write(bytes([212]))
          print('r')
        elif (mx<(1/3*dx)):
          ardu.write(bytes([213]))
          print('l')
        elif (mx>(1/3*dx) and mx<(2/3*dx)):
          ardu.write(bytes([210]))
          print('f')
        else:
          ardu.write(bytes([225]))
          print('if this shows up you made a mistake')
    #else:
    #print("has stuff")
    #print(mx,' ',my)
    #time.sleep(0.1)
    
    
  cv.destroyAllWindows()