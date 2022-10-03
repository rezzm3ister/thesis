import cv2 as cv
import time
import serial
import serial.tools.list_ports

def getport():
  ports=list(serial.tools.list_ports.comports())
  return ports[0].device

ardu=serial.Serial(port=getport(),baudrate=9600,timeout=1)

if __name__ == "__main__":
  vid=cv.VideoCapture(0) #trial and error to find the right cam
  cascade=cv.CascadeClassifier('cascade.xml')
  mx=0
  my=0

  framex=vid.get(cv.CAP_PROP_FRAME_WIDTH)
  framey=vid.get(cv.CAP_PROP_FRAME_HEIGHT)
  cv.namedWindow('img')
  while(True):
    ret,frame=vid.read()
    #frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        
    #cv.imshow('img',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
      break
    
    eyes=cascade.detectMultiScale(frame,scaleFactor=1.10,minNeighbors=20)

    for(x,y,w,h) in eyes:
      mx=x+w/2
      my=y+h/2
      #cv.circle(frame,(250,250),radius=100,color=(0,0,126),thickness=-1)
      
      #cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), thickness=5)
    #cv.circle(frame,(int(framex/2),int(framey/2)),radius=10,color=(255,0,0),thickness=-1)
      cv.rectangle(frame,(x,y),(x+w,y+h),color=(0,0,255),thickness=3)
      #print(x," ",y)
    cv.imshow('img',frame)
    
    if (mx>(2/3*framex)):
      ardu.write(bytes(['r']))
      print('r')
    elif (mx<(1/3*framex)):
      ardu.write(bytes(['l']))
      print('l')
    elif (mx>(1/3*framex) and mx<(2/3*framex)):
      ardu.write(bytes(['f']))
      print('f')
    elif (bool(eyes)==0):
      ardu.write(bytes(['s']))
    else:
      ardu.write(bytes(['n']))
      print('n')
    
    #print(mx,' ',my)

    
  cv.destroyAllWindows()