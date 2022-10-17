import cv2 as cv
import time
import serial
import serial.tools.list_ports
#pip install pyserial
def getport():
  ports=list(serial.tools.list_ports.comports())
  return ports[0].device

#ardu=serial.Serial(port=getport(),baudrate=9600,timeout=1)

if __name__ == "__main__":
  vid=cv.VideoCapture(0) #trial and error to find the right cam
  cascade=cv.CascadeClassifier('cascade-2.xml')
  mx=0
  my=0

  #framex=vid.get(cv.CAP_PROP_FRAME_WIDTH)
  #framey=vid.get(cv.CAP_PROP_FRAME_HEIGHT)

  framex=720
  framey=405
  cv.namedWindow('img')
  while(True):
    ret,frame=vid.read()
    #frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        
    #cv.imshow('img',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
      break
    frame=cv.resize(frame,(720,405))
    signs=cascade.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=9)
    time.sleep(0.01)
    for(x,y,w,h) in signs:
      mx=x+w/2
      my=y+h/2
      #cv.circle(frame,(250,250),radius=100,color=(0,0,126),thickness=-1)
      
      #cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), thickness=5)
    #cv.circle(frame,(int(framex/2),int(framey/2)),radius=10,color=(255,0,0),thickness=-1)
      cv.rectangle(frame,(x,y),(x+w,y+h),color=(0,0,255),thickness=3)
      #print(x," ",y)
    cv.imshow('img',frame)
    '''
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
    '''
    if(signs==()):
      print('s')
    else:
      if (mx>(2/3*framex)):
      #ardu.write(bytes(['r']))
        print('r')
      elif (mx<(1/3*framex)):
        #ardu.write(bytes(['l']))
        print('l')
      elif (mx>(1/3*framex) and mx<(2/3*framex)):
        #ardu.write(bytes(['f']))
        print('f')
      else:
        #ardu.write(bytes(['n']))
        print('n')
    #else:
    #print("has stuff")
    #print(mx,' ',my)

    
  cv.destroyAllWindows()