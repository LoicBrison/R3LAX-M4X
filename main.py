import pygame
from pygame.locals import *
import os
import sys
import time

SCREEN_SIZE = (480, 320)
MARGIN_RATIO = 1/64.0
BORDER_SIZE = 3
X_MARGIN = SCREEN_SIZE[0]*MARGIN_RATIO
Y_MARGIN = SCREEN_SIZE[0]*MARGIN_RATIO

SANS_SPRITE_RECT = (0, 0, 36, 33)

SANS_TEXT_BOX = (0, SCREEN_SIZE[1]-(SCREEN_SIZE[1]/4), SCREEN_SIZE[0], SCREEN_SIZE[1]/4)

if __name__ == '__main__':
	pygame.init()
	surface = pygame.display.set_mode(SCREEN_SIZE, NOFRAME)
	pygame.display.set_caption("")
	doit = True
	textBox = pygame.Rect(SANS_TEXT_BOX[0]+X_MARGIN, SANS_TEXT_BOX[1]+Y_MARGIN, SANS_TEXT_BOX[2]-(Y_MARGIN*2), SANS_TEXT_BOX[3]-(Y_MARGIN*2))
	textBoxInner = pygame.Rect(textBox[0]+3, textBox[1]+3, textBox[2]-(BORDER_SIZE*2), textBox[3]-(BORDER_SIZE*2))
	y = (textBoxInner[3]/2)-(SANS_SPRITE_RECT[3]/2)

	spritesheet = pygame.image.load('sans.png')
	font = pygame.font.Font('undertale.ttf', 18)

	choice0 = font.render('Tripotanus', True, (0, 255, 0))
	choice1 = font.render('Tabouret', True, (0, 0, 255))
	textSans = 'Que veux tu faire ?'
	spriteCount = int(spritesheet.get_width()/SANS_SPRITE_RECT[2])
	t0 = time.time_ns()
	textTimer = 0
	sansTimer = 0
	textSansIndex = 0
	spriteIndex = 1
	while doit:
		t1 = time.time_ns()
		dt = float(t1 - t0)/1000000.0
		t0 = t1
		textTimer += dt
		sansTimer += dt
		if textTimer > 250.0:
			textTimer -= 500.0
			textSansIndex = min(textSansIndex+1, len(textSans))
		if sansTimer > 1000.0:
			sansTimer -= 1000.0
			spriteIndex += 1
			spriteIndex %= spriteCount

		textSansImg = font.render(textSans[0:textSansIndex], True, (255, 255, 255))

		surface.fill((.5*255, 0, 0))
		surface.fill((255, 255, 255), textBox)
		surface.fill((0, 0, 0), textBoxInner)
		surface.blit(spritesheet, (textBoxInner[0]+y, textBoxInner[1]+y), (spriteIndex * SANS_SPRITE_RECT[2], SANS_SPRITE_RECT[1], SANS_SPRITE_RECT[2], SANS_SPRITE_RECT[3]))
		surface.blit(choice0, (36 + 30, (320.0 / 2.0) - (33 / 2.0)))
		surface.blit(choice1, (36 + 30, ((320.0 / 2.0) - (33 / 2.0))+choice0.get_height()+X_MARGIN))
		surface.blit(textSansImg, (SANS_SPRITE_RECT[2]+textBoxInner[0]+(y*2), textBoxInner[1]+((textBoxInner[3]/2)-(textSansImg.get_height()/2))))
		for event in pygame.event.get():
			if event.type == QUIT:
				doit = False
		pygame.display.update()
	pygame.display.quit()
	sys.exit()

def showMainMenu(error):
	os.system('cls')
	if error:
		print("Nani bakayaro ?!!!")
	print("1 - Salut toi !")
	print("2 - Qui est là ?")
	print("3 - Passe un message")
	print("4 - A plus !")

def communicate():
	pass

def whosThere():
	pass

def sendMessage():
	pass

def main():
	doit = True
	error = False
	while doit:
		showMainMenu(error)
		error = False	
		userInput = input()
		try:
			n = int(userInput)
			if n == 1:
				communicate()
			elif n == 2:
				whosThere()
			elif n == 3:
				sendMessage()
			elif n == 4:
				doit = False
			else:
				error = True
		except ValueError as e:
			pass

if __name__ == '__main__':
	pass