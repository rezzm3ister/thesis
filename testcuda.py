import cv2 as cv

vid=cv.VideoCapture(0)

while True:
  ret,frame=vid.read()
  src = cv.cuda_GpuMat()
  src.upload(frame)

  src=cv.cuda.cvtColor(src, cv.COLOR_BGR2GRAY)

  result=src.download()
  if cv.waitKey(1) & 0xFF == ord('q'):
      break
  if result is not None:
    cv.imshow('img',result)

cv.destroyAllWindows()
