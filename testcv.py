import cv2 as cv

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
      print(x," ",y)
    cv.imshow('img',frame)
    

    #print(mx,' ',my)

    
  cv.destroyAllWindows()