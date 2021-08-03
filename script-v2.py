import math
import numpy as np, cv2

width = 300
height = 400

M2 = 0

#quatro pontos iniciais dos corners do grid
referencePoints = np.float32([[width/4,height/4],[3*width/4,height/4],[3*width/4,3*height/4],[width/4,3*height/4]])
#referencePoints = np.float32([[150,150],[250,150],[250,250],[150,250]])

currentPoint = -1 #indica qual dos 4 pontos atuais estah selecionado
calibrating = True #indica se o modo de calibracao estah ativado
fullScreen = False #indica se o modo de tela cheia estah ativado

# inputimage1 = cv2.imread("grid.png") # le a imagem do grid
inputimage1 = cv2.imread("fluxometro.jpg") # le a imagem do grid
inputimage1 = cv2.resize(inputimage1, (width,height))
scale = cv2.imread("scale2.png") # le a imagem da escala de cor
rows1, cols1 = inputimage1.shape[:2] # le as dimensoes do grid
pts1 = np.float32([[0,0],[cols1,0],[cols1,rows1],[0,rows1]]) #cria os pontos de controle para a imagem do grid
image = np.zeros((height, width, 3), np.uint8) #cria uma imagem colorida para a tela


#funcao que retorna a cor de um corner especifico para a calibracao
def pointColor(n):
	if n == 0:
		return (0,0,255)
	elif n == 1:
		return (0,255,255)
	elif n == 2:
		return (255,255,0)
	else:
		return (0,255,0)

#esta funcao eh chamada sempre que um evento de mouse acontece (clicar, arrastar, soltar, etc)
def mouse(event, x, y, flags, param):
	if(not calibrating):
		return
	global currentPoint
	
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

#cria a janela principal da aplicacao
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
#associa uma funcao de eventos do mouse a janela principal criada
cv2.setMouseCallback("test", mouse)

#diz que a cor selecionada inicialmente eh branco

#loop principal
while True:
	image[:] = inputimage1 #limpa a imagem (pinta toda ela de preto)
		
	if calibrating: #se estiver com o modo de calibracao ativado, pinta os pontos coloridos em cada corner do grid
		color = 0
		for point in referencePoints:
			cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)
			color = color + 1

	M = cv2.getPerspectiveTransform(pts1,referencePoints) # calcula a projecao com base nas coordenadas dos 4 corners
	M2 = cv2.getPerspectiveTransform(referencePoints, pts1) # calcula a projecao com base nas coordenadas dos 4 corners	

	cv2.imshow("test", image) #exibe a imagem na tela
	key = cv2.waitKey(1) & 0xFF #espera 1ms e verifica se alguma tecla foi pressionada

	if key == ord("c"): #caso a tecla 'c' tenha sido pressionada, habilita ou desabilita o modo de calibracao
		calibrating = not calibrating

	if key == ord("f"): #caso a tecla 'f' tenha sido pressionada, habilita ou desabilita o modo de tela cheia
		if fullScreen == False:
			cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		else:
			cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
		fullScreen = not fullScreen

	if key == ord("q"): #caso a tecla 'q' tenha sido pressionada, fecha a aplicacao
		break

cv2.destroyAllWindows()
