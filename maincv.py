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

def getdispsum(depth):
  dmx=vx//8
  dmy=vy//8
  dmat=np.zeros((8,8))

  dmat[0,0]=np.sum(depth[0:17,0:31])
  dmat[0,1]=np.sum(depth[0:17,32:63])
  dmat[0,2]=np.sum(depth[0:17,64:95])
  dmat[0,3]=np.sum(depth[0:17,96:127])
  dmat[0,4]=np.sum(depth[0:17,128:159])
  dmat[0,5]=np.sum(depth[0:17,160:191])
  dmat[0,6]=np.sum(depth[0:17,192:221])
  dmat[0,7]=np.sum(depth[0:17,224:255])

  dmat[1,0]=np.sum(depth[18:35,0:31])
  dmat[1,1]=np.sum(depth[18:35,32:63])
  dmat[1,2]=np.sum(depth[18:35,64:95])
  dmat[1,3]=np.sum(depth[18:35,96:127])
  dmat[1,4]=np.sum(depth[18:35,128:159])
  dmat[1,5]=np.sum(depth[18:35,160:191])
  dmat[1,6]=np.sum(depth[18:35,192:221])
  dmat[1,7]=np.sum(depth[18:35,224:255])

  dmat[2,0]=np.sum(depth[36:53,0:31])
  dmat[2,1]=np.sum(depth[36:53,32:63])
  dmat[2,2]=np.sum(depth[36:53,64:95])
  dmat[2,3]=np.sum(depth[36:53,96:127])
  dmat[2,4]=np.sum(depth[36:53,128:159])
  dmat[2,5]=np.sum(depth[36:53,160:191])
  dmat[2,6]=np.sum(depth[36:53,192:221])
  dmat[2,7]=np.sum(depth[36:53,224:255])

  dmat[3,0]=np.sum(depth[54:71,0:31])
  dmat[3,1]=np.sum(depth[54:71,32:63])
  dmat[3,2]=np.sum(depth[54:71,64:95])
  dmat[3,3]=np.sum(depth[54:71,96:127])
  dmat[3,4]=np.sum(depth[54:71,128:159])
  dmat[3,5]=np.sum(depth[54:71,160:191])
  dmat[3,6]=np.sum(depth[54:71,192:221])
  dmat[3,7]=np.sum(depth[54:71,224:255])

  dmat[4,0]=np.sum(depth[72:89,0:31])
  dmat[4,1]=np.sum(depth[72:89,32:63])
  dmat[4,2]=np.sum(depth[72:89,64:95])
  dmat[4,3]=np.sum(depth[72:89,96:127])
  dmat[4,4]=np.sum(depth[72:89,128:159])
  dmat[4,5]=np.sum(depth[72:89,160:191])
  dmat[4,6]=np.sum(depth[72:89,192:221])
  dmat[4,7]=np.sum(depth[72:89,224:255])

  dmat[5,0]=np.sum(depth[90:125,0:31])//2
  dmat[5,1]=np.sum(depth[90:125,32:63])//2
  dmat[5,2]=np.sum(depth[90:125,64:95])//2
  dmat[5,3]=np.sum(depth[90:125,96:127])//2
  dmat[5,4]=np.sum(depth[90:125,128:159])//2
  dmat[5,5]=np.sum(depth[90:125,160:191])//2
  dmat[5,6]=np.sum(depth[90:125,192:221])//2
  dmat[5,7]=np.sum(depth[90:125,224:255])//2

  dmat[6,0]=np.sum(depth[126:143,0:31])
  dmat[6,1]=np.sum(depth[126:143,32:63])
  dmat[6,2]=np.sum(depth[126:143,64:95])
  dmat[6,3]=np.sum(depth[126:143,96:127])
  dmat[6,4]=np.sum(depth[126:143,128:159])
  dmat[6,5]=np.sum(depth[126:143,160:191])
  dmat[6,6]=np.sum(depth[126:143,192:221])
  dmat[6,7]=np.sum(depth[126:143,224:255])

  dmat[7,0]=np.sum(depth[126:144,0:31])
  dmat[7,1]=np.sum(depth[126:144,32:63])
  dmat[7,2]=np.sum(depth[126:144,64:95])
  dmat[7,3]=np.sum(depth[126:144,96:127])
  dmat[7,4]=np.sum(depth[126:144,128:159])
  dmat[7,5]=np.sum(depth[126:144,160:191])
  dmat[7,6]=np.sum(depth[126:144,192:221])
  dmat[7,7]=np.sum(depth[126:144,224:255])

  return dmat



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



    
    #DEPTH MAP
    dfl=cv.resize(fl,(vx,vy))
    dfr=cv.resize(fr,(vx,vy))
    stereo=cv.cuda.StereoSGM.create(minDisparity=10,numDisparities=32,blockSize=16,speckleRange=4)
    depth=stereo.compute(dfl,dfr)
    depth=depth
    cv.imshow("depth",depth/1280)

    #depth regions
    dmat=np.zeros((8,8))
    dmx=vx//8
    dmy=vy//8

    #refer to function above
    dmat=getdispsum(depth)

    nearcount=(dmat>200000).sum()

    if(nearcount>10):
      print("something ahead")
    elif(nearcount>20):
      print("stop pls")
    elif(nearcount>30):
      print("BLOODY FUCKING STOP")
    else:
      print("this is fine")


    #print(dmat)
    print("regions above threshold: ",nearcount)
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