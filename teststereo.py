import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

sx=640
sy=360

left=cv2.VideoCapture(0)
right=cv2.VideoCapture(1)
left.set(cv2.CAP_PROP_FRAME_WIDTH, sx)
left.set(cv2.CAP_PROP_FRAME_HEIGHT, sy)
right.set(cv2.CAP_PROP_FRAME_WIDTH, sx)
right.set(cv2.CAP_PROP_FRAME_HEIGHT, sy)
gl=cv2.cuda_GpuMat()
gr=cv2.cuda_GpuMat()
gd=cv2.cuda_GpuMat()
font = cv2.FONT_HERSHEY_SIMPLEX

ft=0
pft=0
print(cv2.cuda.getCudaEnabledDeviceCount())

while True:

  
  retl,fl=left.read()

  retr,fr=right.read()
  
  #stereo=cv2.StereoSGBM.create(numDisparities=64,blockSize=16,speckleRange=16)
  stereo=cv2.cuda.StereoSGM.create(minDisparity=10,numDisparities=128,blockSize=8,speckleRange=2)


  #fl=cv2.cvtColor(fl,cv2.COLOR_BGR2GRAY)
  #fr=cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY)
  #gl.upload(fl)
  #gr.upload(fr)
  depth=stereo.compute(fl,fr)

  ft=time.time()

  fps=1/(ft-pft)
  cv2.putText(depth, str(fps), (7, 70), font, 1, 255, 3, cv2.LINE_AA)
  pft=ft


  #cv2.imshow("left",fl)
  #cv2.imshow("right",fr)

  #plt.imshow(depth,'gray')
  #plt.show()

  cv2.imshow("depth",depth/1280)
  if cv2.waitKey(1) & 0xFF == ord('q'):
	  break


