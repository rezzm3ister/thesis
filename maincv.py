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

#sign detection size
dx=640
dy=360

#depth detect size
vx=256
vy=144

#get arduino port
def getport():
  ports=list(serial.tools.list_ports.comports())
  return ports[0].device

#ARDUINO CONNECT, UNCOMMENT LINE BELOW FOR ARDUINO
#ardu=serial.Serial(port=getport(),baudrate=9600,timeout=1)

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

  cascade=cv.CascadeClassifier('cascade-2.xml')
  mx=0
  my=0

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
    #cascade detector
    signs=cascade.detectMultiScale(DMSframe,scaleFactor=1.1,minNeighbors=5)
    #allow color again for boxing    
    DMSframe=cv.cvtColor(DMSframe,cv.COLOR_GRAY2BGR)
    for(x,y,w,h) in signs:
      mx=x+w/2
      my=y+h/2
      #box the sign
      cv.rectangle(DMSframe,(x,y),(x+w,y+h),color=(0,0,255),thickness=3)
      #print(x," ",y)
    cv.imshow('img',DMSframe)



    '''
    depth matrix regions

    a 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    -------------------------------
    b 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    ------------------------------
    c 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    ------------------------------
    d 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    ------------------------------
    e 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    ------------------------------
    f 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    ------------------------------
    g 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    ------------------------------
    h 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    '''
    #DEPTH MAP
    dfl=cv.resize(fl,(vx,vy))
    dfr=cv.resize(fr,(vx,vy))
    stereo=cv.cuda.StereoSGM.create(minDisparity=10,numDisparities=32,blockSize=16,speckleRange=4)
    depth=stereo.compute(dfl,dfr)
    cv.imshow("depth",depth/1280)

    #depth regions
    dmat=np.zeros((8,8))
    dmx=vx//8
    dmy=vy//8

    for j in range(8):
      for i in range(8):
        td=depth[(dmx*j):(dmx*(j+1)),(dmx*i):(dmx*(i+1))]
        dmat[j,i]=np.sum(td)
        #print(j,"j,",dmx,", ",dmx*j, ", ",dmat[j,i])
      #print(i,"i,",dmy,", ",dmy*i)


    print(depth)
    print(" ")
    #detect closeness




    #FPS COUNTER
    ft=time.time()
    fps=1/(ft-pft)
    #cv.putText(depth, str(fps), (7, 70), font, 1, 255, 3, cv.LINE_AA)
    #print(fps)
    pft=ft



    
    #SEND DATA TO ARDUINO
    #uncomment after
    '''
    if(signs==()):
      print('s')
      #ardu.write(bytes(['s']))
    else:
      print(mx," ",my)
      if (mx>(2/3*dx)):
      #ardu.write(bytes(['r']))
        print('r')
      elif (mx<(1/3*dx)):
        #ardu.write(bytes(['l']))
        print('l')
      elif (mx>(1/3*dx) and mx<(2/3*dx)):
        #ardu.write(bytes(['f']))
        print('f')
      else:
        #ardu.write(bytes(['n']))
        print('n')
    #else:
    #print("has stuff")
    #print(mx,' ',my)
    '''
    
  cv.destroyAllWindows()