#%matplotlib inline
import cv2 # OpenCV
import matplotlib.pyplot as plt # Matplotlib
import numpy as np, cv2 # Numpy
import math
img = cv2.imread('media/Img3/IMG_20200121_151250.jpg')
width = 300
height = 400
img = cv2.resize(img, (width,height))
fullScreen = False
calibrating = True #indica se o modo de calibracao estah ativado
referencePoints = np.float32([[width/4,height/4],[3*width/4,height/4],[3*width/4,3*height/4],[width/4,3*height/4]])
currentPoint = -1 #indica qual dos 4 pontos atuais estah selecionado

def pointColor(n):
	if n == 0:
		return (0,0,255)
	elif n == 1:
		return (0,255,255)
	elif n == 2:
		return (255,255,0)
	else:
		return (0,255,0)


def mouse(event, x, y, flags, param):
	global currentPoint
	print(x, y, currentPoint)
	#if(not calibrating):
	#	return

	if event == cv2.EVENT_LBUTTONDOWN:
		cp = 0
  	#descobre em qual dos 4 pontos o usuario clicou (precisa estar a uma distancia maxima de 4 pixels para ser considerado o clique)
		for point in referencePoints:
			dist = math.sqrt((x-point[0])*(x-point[0])+(y-point[1])*(y-point[1]))
			if dist < 4:
				currentPoint = cp
				break
			else:
				cp = cp + 1

	if event == cv2.EVENT_LBUTTONUP: #quando o clique é solto, diz o que o ponto selecionado eh -1
		currentPoint = -1
		
	if currentPoint != -1: #move as coordenadas do ponto selecionado para a posicao lida do mouse
		referencePoints[currentPoint] = [x,y]
		
cv2.namedWindow("test")		
cv2.setMouseCallback("test", mouse)

while(True):
	cv2.imshow("test", img)
	key = cv2.waitKey(10) & 0xFF
	if key == ord('q'):
		break
	elif key == ord("c"): 
		calibrating = not calibrating

	if calibrating: 
		color = 0
		for point in referencePoints:
			cv2.circle(img, (int(point[0]), int(point[1])),5,pointColor(color), -1)
			color = color + 1

	
