import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import time

sx=1280
sy=720
vx=256
vy=144

left=cv.VideoCapture(0)
right=cv.VideoCapture(1)
left.set(cv.CAP_PROP_FRAME_WIDTH, sx)
left.set(cv.CAP_PROP_FRAME_HEIGHT, sy)
right.set(cv.CAP_PROP_FRAME_WIDTH, sx)
right.set(cv.CAP_PROP_FRAME_HEIGHT, sy)
gl=cv.cuda_GpuMat()
gr=cv.cuda_GpuMat()
gd=cv.cuda_GpuMat()
font = cv.FONT_HERSHEY_SIMPLEX

ft=0
pft=0
print(cv.cuda.getCudaEnabledDeviceCount())

while True:

  
  retl,fl=left.read()

  retr,fr=right.read()
  
  fl=cv.resize(fl,(vx,vy))
  fr=cv.resize(fr,(vx,vy))

  #stereo=cv2.StereoSGBM.create(numDisparities=64,blockSize=16,speckleRange=16)
  stereo=cv.cuda.StereoSGM.create(minDisparity=10,numDisparities=32,blockSize=16,speckleRange=4)


  fl=cv.cvtColor(fl,cv.COLOR_BGR2GRAY)
  fr=cv.cvtColor(fr,cv.COLOR_BGR2GRAY)
  #gl.upload(fl)
  #gr.upload(fr)
  depth=stereo.compute(fl,fr)

  ft=time.time()

  fps=1/(ft-pft)
  cv.putText(depth, str(fps), (7, 70), font, 1, 255, 3, cv.LINE_AA)
  pft=ft


  #cv2.imshow("left",fl)
  #cv2.imshow("right",fr)

  #plt.imshow(depth,'gray')
  #plt.show()

  cv.imshow("depth",depth/1280)
  if cv.waitKey(1) & 0xFF == ord('q'):
	  break


