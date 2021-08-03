import math
import numpy as np, cv2
width = 300
height = 400
M2 = 0
referencePoints = np.float32([[width/4,height/4],[3*width/4,height/4],[3*width/4,3*height/4],[width/4,3*height/4]])
currentPoint = -1 
calibrating = True 
fullScreen = False 
inputimage1 = cv2.imread("fluxometro.jpg") 
inputimage1 = cv2.resize(inputimage1, (width,height))
scale = cv2.imread("scale2.png") 
rows1, cols1 = inputimage1.shape[:2] 
pts1 = np.float32([[0,0],[cols1,0],[cols1,rows1],[0,rows1]]) 
image = np.zeros((height, width, 3), np.uint8) 
def pointColor(n):
  if n == 0: return (0,0,255)
  elif n == 1: return (0,255,255)
  elif n == 2: return (255,255,0)
  else: return (0,255,0)
def mouse(event, x, y, flags, param):
  if(not calibrating): return
  global currentPoint
  if event == cv2.EVENT_LBUTTONDOWN:
    cp = 0
    for point in referencePoints:
      dist = math.sqrt((x-point[0])*(x-point[0])+(y-point[1])*(y-point[1]))
      if dist < 4:
        currentPoint = cp
        break
      else:
        cp = cp + 1
  if event == cv2.EVENT_LBUTTONUP: currentPoint = -1
  if currentPoint != -1: referencePoints[currentPoint] = [x,y]
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("test", mouse)
while True:
  image[:] = inputimage1 
  if calibrating: 
    color = 0
    for point in referencePoints:
      cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)
      color = color + 1
  M = cv2.getPerspectiveTransform(pts1,referencePoints) 
  M2 = cv2.getPerspectiveTransform(referencePoints, pts1)
  cv2.imshow("test", image) 
  key = cv2.waitKey(1) & 0xFF
  if key == ord("c"): calibrating = not calibrating
  if key == ord("f"): 
    cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL if fullScreen else cv2.WINDOW_FULLSCREEN)
    fullScreen = not fullScreen
  if key == ord("q"): break
cv2.destroyAllWindows()
