#!/bin/python
import numpy as np, cv2
import math
width = 300
height = 400
referencePoints = np.float32([[38*width/100,24*height/100],[52*width/100,24*height/100],[52*width/100,73*height/100],[38*width/100,73*height/100]])
currentPoint = -1
fullScreen = False
# inputimage1 = cv2.imread("media/Img3/IMG_20200121_151305.jpg")
# inputimage1 = cv2.imread("media/Img3/IMG_20200121_151233.jpg")
# inputimage1 = cv2.imread("media/Img3/IMG_20200121_151233.jpg")
# inputimage1 = cv2.imread("media/Img3/IMG_20200121_151240.jpg")
# inputimage1 = cv2.imread("media/Img3/IMG_20200121_151252.jpg")
# inputimage1 = cv2.imread("media/Img1/IMG_20200120_140536.jpg")
inputimage1 = cv2.imread("flowmeter.jpg")
inputimage1 = cv2.resize(inputimage1, (width,height))
number = 0
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
  # Corners {{{
  inputimage1_copy = inputimage1.copy()
  x1 = int((referencePoints[0][0] + referencePoints[3][0])/2)
  x2 = int((referencePoints[1][0] + referencePoints[2][0])/2)
  y1 = int((referencePoints[0][1] + referencePoints[1][1])/2)
  y2 = int((referencePoints[3][1] + referencePoints[2][1])/2)
  referencePoints2 = np.float32([[x1,y1],[x2,y1],[x2,y2],[x1,y2]])
  width2 = int(height*(x2-x1)/(y2-y1))
  if width2 > width: width2 = width
  #}}}
  # Generate Image {{{
  image = np.zeros((height, width+width2, 3), np.uint8)
  image[:] = (0,0,0)
  #}}}
  # Perspective {{{
  fatia = np.zeros((height, width2, 3), np.uint8)
  pts1 = np.float32([[0,0],[width2,0],[width2,height],[0,height]])
  color = 0
  M2 = cv2.getPerspectiveTransform(referencePoints2, pts1)
  cv2.warpPerspective(inputimage1_copy, M2, (width2,height), fatia, borderMode=cv2.BORDER_TRANSPARENT)
  fatia_copy = fatia.copy()
  gray = cv2.cvtColor(fatia_copy, cv2.COLOR_BGR2GRAY)
  #}}}
  #Center of mass {{{
  (thresh, circles_binary) = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
  circles_openning = cv2.morphologyEx(circles_binary, cv2.MORPH_OPEN, np.ones((13,5)))
  M = cv2.moments(circles_openning)
  cX = int(M["m10"] / M["m00"]) if M["m10"] != M["m00"] else 0
  cY = int(M["m01"] / M["m00"]) if M["m01"] != M["m00"] else 0

  # }}}
  # Lines {{{
  lines_sobel = cv2.Sobel(gray,cv2.CV_8U,0,2,ksize=5)
  lines_opening = cv2.morphologyEx(lines_sobel, cv2.MORPH_OPEN, np.ones((2,24)))
  (thresh, lines_binary) = cv2.threshold(lines_opening, 160, 255, cv2.THRESH_BINARY)
  lines = cv2.HoughLines(lines_binary, 1, np.pi /2 , 20)
  lines_height = []
  if not (lines is None):
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
      cv2.line(fatia_copy, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
      lines_height += [(pt1[1]+pt2[1])/2]
    lines_height.sort(reverse=True)
  #}}}
  # Find number {{{
  for LM in range(1, len(lines_height)):
    if cY <=lines_height[LM-1]  and cY > lines_height[LM]:
      decimal = (lines_height[LM-1] - cY)/(lines_height[LM-1] - lines_height[LM])
      number = round(LM+decimal, 3)
      print(number)
  #}}}
  # Print center of mass {{{
  cv2.circle(circles_openning, (cX, cY), 2, (0,0,255), -1)
  redImg = np.zeros(fatia_copy.shape, image.dtype)
  redImg[:] = (255, 255, 0)
  redMask = cv2.bitwise_and(redImg, redImg, mask=circles_openning)
  cv2.addWeighted(redMask, 1, fatia_copy, 1, 0, fatia_copy)
  #}}}
  # Print number {{{
  if number > 0:
    cv2.putText(inputimage1_copy, str(number), (25, 45),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)
  #}}}
  #Printa Imagem
  image[0:height,0:width] = inputimage1_copy
  image[0:height,width:width+width2] = fatia_copy
  #}}}
  # Reference points
  for point in referencePoints:
    cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)
    color += 1
  cv2.imshow("test", image)
  # }}}
  # Keyboard
  key = cv2.waitKey(1) & 0xFF
  if key == ord("f"):
    cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL if fullScreen else cv2.WINDOW_FULLSCREEN)
    fullScreen = not fullScreen
  if key == ord("q"): break
cv2.destroyAllWindows()
  #}}}
