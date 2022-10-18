import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

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



if __name__ == "__main__":
  #vid=cv.VideoCapture(0, cv.CAP_DSHOW) #trial and error to find the right cam
  vid=cv.VideoCapture(0)
  cascade=cv.CascadeClassifier('cascade-2.xml')
  mx=0
  my=0
  vid.set(cv.CAP_PROP_FRAME_WIDTH,1280)
  vid.set(cv.CAP_PROP_FRAME_HEIGHT,720)
  #framex=vid.get(cv.CAP_PROP_FRAME_WIDTH)
  #framey=vid.get(cv.CAP_PROP_FRAME_HEIGHT)

  while True:

    if cv.waitKey(1) & 0xFF == ord('q'):
      break

    ret,frame=vid.read()
    frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    c1=frame[0:240,0:426]
    cv.imshow('img',c1)
    print(np.sum(c1))


  cv.destroyAllWindows()



