#!/bin/python
import numpy as np, cv2
import math
width = 300
height = 400
# referencePoints = np.float32([[width/4,height/4],[3*width/4,height/4],[3*width/4,3*height/4],[width/4,3*height/4]])
referencePoints = np.float32([[38*width/100,24*height/100],[52*width/100,24*height/100],[52*width/100,73*height/100],[38*width/100,73*height/100]])
currentPoint = -1 
fullScreen = False 
inputimage1 = cv2.imread("media/Img3/IMG_20200121_151305.jpg")
inputimage1 = cv2.resize(inputimage1, (width,height))
def pointColor(n):
  if n == 0: return (0,0,255)
  elif n == 1: return (0,255,255)
  elif n == 2: return (255,255,0)
  else: return (0,255,0)
def mouse(event, x, y, flags, param):
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

cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("test", mouse)
while True:
  x1 = int((referencePoints[0][0] + referencePoints[3][0])/2)
  x2 = int((referencePoints[1][0] + referencePoints[2][0])/2)
  y1 = int((referencePoints[0][1] + referencePoints[1][1])/2)
  y2 = int((referencePoints[3][1] + referencePoints[2][1])/2)
  referencePoints2 = np.float32([[x1,y1],[x2,y1],[x2,y2],[x1,y2]])
  width2 = int(height*(x2-x1)/(y2-y1))
  if width2 > width: width2 = width
  image = np.zeros((height, width+width2, 3), np.uint8) 
  image[:] = (0,0,0)
  image[0:height,0:width] = inputimage1 
  fatia = np.zeros((height, width2, 3), np.uint8) 
  pts1 = np.float32([[0,0],[width2,0],[width2,height],[0,height]]) 
  color = 0
  for point in referencePoints:
    cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)
    color += 1
  M2 = cv2.getPerspectiveTransform(referencePoints2, pts1)
  cv2.warpPerspective(inputimage1, M2, (width2,height), fatia, borderMode=cv2.BORDER_TRANSPARENT) 
  gray = cv2.cvtColor(fatia, cv2.COLOR_BGR2GRAY)
  lines_fatia = fatia.copy()
  # bordas = cv2.Canny(cinza, 50, 200)
  k1 = np.ones((2,24))
  lines_sobel = cv2.Sobel(gray,cv2.CV_8U,0,2,ksize=5)
  lines_opening = cv2.morphologyEx(lines_sobel, cv2.MORPH_OPEN, k1)
  (thresh, lines_binary) = cv2.threshold(lines_opening, 160, 255, cv2.THRESH_BINARY)
  lines = cv2.HoughLines(lines_binary, 1, np.pi /2 , 20)
  for i in range(0, len(lines)):
    rho = lines[i][0][0]
    theta = lines[i][0][1]
    if theta < 1: continue
    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    cv2.line(lines_fatia, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
  # mask = cv2.inRange(hsv, (0,0,0), (190,190,190))
  # result = cv2.bitwise_not(bordas_copia, fatia, mask=bordas)
  Z = gray
  Z = np.float32(Z)
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
  K=19
  ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
  center = np.uint8(center)
  res = center[label.flatten()]
  res2 = res.reshape((gray.shape))
  # img_b = cv2.GaussianBlur(gray, (3, 3), 15)
  # laplacian = cv2.Laplacian(img_b, cv2.CV_64F)
  # (thresh, circles_binary) = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
  # circles_blur = cv2.medianBlur(gray,5)
  # circles_canny = cv2.Canny(gray, 50, 200)
  # circles = cv2.HoughCircles(circles_binary, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100)
  # print(circles)
  # if circles is not None:
  #   circles = np.round(circles[0, :]).astype("int")
  #   for circle in circles:
  #     # print(circle)
  #     print('(%d, %d) com raio %d' % (circle[0], circle[1], circle[2]))
  #   for (x, y, r) in circles:
  #     cv2.circle(fatia, (x, y), r, (0, 0, 255), 4)
  image[0:height,width:width+width2] = fatia 
  cv2.imshow("test", image) 
  cv2.imshow("circle", res2) 
  # cv2.imshow("circle", circles_canny) 
  key = cv2.waitKey(1) & 0xFF
  if key == ord("f"): 
    cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL if fullScreen else cv2.WINDOW_FULLSCREEN)
    fullScreen = not fullScreen
  if key == ord("q"): break
cv2.destroyAllWindows()
