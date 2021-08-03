#!/bin/python
import math
import numpy as np, cv2
width = 300
height = 400
referencePoints = np.float32([[width/4,height/4],[3*width/4,height/4],[3*width/4,3*height/4],[width/4,3*height/4]])
currentPoint = -1 
fullScreen = False 
inputimage1 = cv2.imread("media/Img3/IMG_20200121_151305.jpg")
inputimage1 = cv2.resize(inputimage1, (width,height))
#cv2.imshow("teste", inputimage1);
#cv2.waitKey(0) 
image = np.zeros((height, 2*width, 3), np.uint8) 
image2 = np.zeros((height, 2*width, 3), np.uint8) 
fatia = np.zeros((height, width, 3), np.uint8) 
def pointColor(n):
  if n == 0: return (0,0,255)
  elif n == 1: return (0,255,255)
  elif n == 2: return (255,255,0)
  else: return (0,255,0)
def mouse(event, x, y, flags, param):
  global fatia
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
  if event == cv2.EVENT_LBUTTONUP:
    currentPoint = -1
  if currentPoint != -1: referencePoints[currentPoint] = [x,y]
  # pt1 = [int((referencePoints[0][0] + referencePoint[2][0])/2), int((referencePoints[0][1] + referencePoint[1][1])/2) ]
  # pt2 = [int((referencePoints[1][0] + referencePoint[3][0])/2), int((referencePoints[2][1] + referencePoint[3][1])/2) ]
  # fatia = inputimage1[pt1, pt2]
  #fatia[:] = (255,0,255)
  #print(fatia.shape)

# fatia = inputimage1.copy()
height2 = 400
width2 = 300
#fatia = inputimage1[0:height2, 0:width2]
proporcao=int(height/height2)
rows1, cols1 = fatia.shape[:2] # le as dimensoes do grid
pts1 = np.float32([[0,0],[cols1,0],[cols1,rows1],[0,rows1]]) #cria os pontos de controle para a imagem do grid
mypoints = np.float32([[width,0],[2*width,0],[2*width,height],[width,height]])
print( pts1)

cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("test", mouse)
while True:
  # print("0:",height,",", width,":",width+proporcao*width2)
  image[:] = (0,0,0)
  image[0:height,0:width] = inputimage1 
  # image[0:height,width:2*width] = fatia
  # image[0:40,width:width+30] = fatia
  # image[0:height,width:width+(proporcao*width2)] = fatia
  color = 0
  for point in referencePoints:
    cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)
    color = color + 1
  M = cv2.getPerspectiveTransform(pts1,mypoints)
  # print(M)
  M2 = cv2.getPerspectiveTransform(referencePoints, pts1)
  print(width, height)
  #cv2.warpPerspective(fatia, M, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT) 
  cv2.warpPerspective(inputimage1, M2, (width,height), fatia, borderMode=cv2.BORDER_TRANSPARENT) 
  image[0:height,width:width*2] = fatia 
  cv2.imshow("input", inputimage1) 
  cv2.imshow("test", image) 
  cv2.imshow("fatia", fatia) 
  key = cv2.waitKey(1) & 0xFF
  if key == ord("f"): 
    cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL if fullScreen else cv2.WINDOW_FULLSCREEN)
    fullScreen = not fullScreen
  if key == ord("q"): break
cv2.destroyAllWindows()
