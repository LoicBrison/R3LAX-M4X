import math

import pygame
from pygame.locals import *
import os
import sys
import time
import math

SCREEN_SIZE = (480, 320)
MARGIN_RATIO = 1/64.0
BORDER_SIZE = 3
X_MARGIN = SCREEN_SIZE[0]*MARGIN_RATIO
Y_MARGIN = SCREEN_SIZE[0]*MARGIN_RATIO

SANS_SPRITE_RECT = (0, 0, 36, 33)

SANS_TEXT_BOX = (0, SCREEN_SIZE[1]-(SCREEN_SIZE[1]/4), SCREEN_SIZE[0], SCREEN_SIZE[1]/4)

CHOICES = [
	"Nani bakayaro ?!!!",
	"Salut toi !",
	"Qui est la ?",
	"Passe un message",
	"A plus !",
]

INITIAL_PROMPT = "Que veux tu faire ?"

if __name__ == '__main__':
	pygame.init()

	flags = pygame.NOFRAME | pygame.FULLSCREEN
	if len(sys.argv) > 1 and sys.argv[1].lower() == 'debug': flags &= ~pygame.FULLSCREEN
	surface = pygame.display.set_mode(SCREEN_SIZE, flags)
	pygame.display.set_caption("")
	doit = True
	textBox = pygame.Rect(SANS_TEXT_BOX[0]+X_MARGIN, SANS_TEXT_BOX[1]+Y_MARGIN, SANS_TEXT_BOX[2]-(Y_MARGIN*2), SANS_TEXT_BOX[3]-(Y_MARGIN*2))
	textBoxInner = pygame.Rect(textBox[0]+3, textBox[1]+3, textBox[2]-(BORDER_SIZE*2), textBox[3]-(BORDER_SIZE*2))
	y = (textBoxInner[3]/2)-(SANS_SPRITE_RECT[3]/2)

	textX = SANS_SPRITE_RECT[2] + textBoxInner[0] + (y * 2)

	spritesheet = pygame.image.load('sans.png')
	arrowLeft = pygame.image.load('arrow.png')
	arrowBottom = pygame.transform.rotate(arrowLeft, -90)
	font = pygame.font.Font('undertale.ttf', 18)

	choices = [font.render(c, True, (255, 255, 255)) for c in CHOICES]

	textSans = INITIAL_PROMPT
	spriteCount = int(spritesheet.get_width()/SANS_SPRITE_RECT[2])
	t0 = time.time_ns()
	textTimer = 0
	sansTimer = 0
	textSansIndex = 0
	spriteIndex = 1

	height = choices[0].get_height()
	for c in choices: assert height == c.get_height()

	arrowX = textX-(arrowLeft.get_width() + X_MARGIN)
	arrowTopY = (height/2) - (arrowLeft.get_height() / 2)
	choicesBaseY = X_MARGIN*2
	textOffsetY = height+X_MARGIN
	fittingCount = int(math.floor((surface.get_height()-((surface.get_height()-textBox.y)+choicesBaseY))/(height+choicesBaseY)))
	choicesRect = pygame.Rect(arrowX, choicesBaseY, surface.get_width()-(arrowX*2), surface.get_height()-((surface.get_height()-textBox.y)+choicesBaseY*2))
	arrowBottomX = (surface.get_width() - (arrowX * 2))-(arrowBottom.get_width()/2)
	choicesHitBox = [pygame.Rect(textX, choicesBaseY+(textOffsetY*i), c.get_width(), c.get_height()) for i, c in enumerate(choices)]

	currentSelectedText = 0

	shownChoices = min(len(CHOICES), fittingCount)

	arrowTimer = 400.0
	doAction = 0
	actionTimer = 0.0
	while doit:
		t1 = time.time_ns()
		dt = float(t1 - t0)/1000000.0
		t0 = t1
		textTimer += dt
		sansTimer += dt
		arrowTimer += dt


		if doAction == 2: actionTimer += dt

		if actionTimer > 1000.0:
			if currentSelectedText == 2:
				textSans = INITIAL_PROMPT
				textSansIndex = 0
			elif currentSelectedText == 4:
				doit = False
			doAction = 0
			spriteIndex = 0
			actionTimer = 0

		if textTimer > 100.0:
			textTimer -= 100.0
			textSansIndex = min(textSansIndex+1, len(textSans))
			while len(textSans) > textSansIndex and textSans[textSansIndex].isspace():
				textSansIndex = min(textSansIndex + 1, len(textSans))

		if textSansIndex == len(textSans) and doAction == 1: doAction = 2


		if sansTimer > 1000.0 and doAction == 0:
			sansTimer -= 1000.0
			spriteIndex += 1
			spriteIndex %= spriteCount
		if arrowTimer > 1200.0 and doAction == 0:
			arrowTimer -= 1200.0

		textSansImg = font.render(textSans[0:textSansIndex], True, (255, 255, 255))

		surface.fill((0, 0, 0))
		surface.fill((255*0.5, 255*0.5, 255*0.5), choicesRect)

		choiceY = choicesBaseY
		for i, c in enumerate(choices[0:fittingCount]):
			surface.blit(c, (textX, choiceY))
			choiceY += textOffsetY

		surface.fill((255, 255, 255), textBox)
		surface.fill((0, 0, 0), textBoxInner)
		surface.blit(spritesheet, (textBoxInner[0]+y, textBoxInner[1]+y), (spriteIndex * SANS_SPRITE_RECT[2], SANS_SPRITE_RECT[1], SANS_SPRITE_RECT[2], SANS_SPRITE_RECT[3]))
		surface.blit(textSansImg, (textX, textBoxInner[1]+((textBoxInner[3]/2)-(textSansImg.get_height()/2))))
		if arrowTimer >= 400.0:
			surface.blit(arrowLeft, (arrowX, arrowTopY + choicesBaseY + (textOffsetY * currentSelectedText)))
		if len(CHOICES) > fittingCount:
			surface.blit(arrowBottom, (((surface.get_width() - arrowBottom.get_width()) / 2, choiceY)))

		if doAction == 0:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					for i, hitbox in enumerate(choicesHitBox):
						if event.pos[0] >= hitbox.x and event.pos[1] >= hitbox.y and event.pos[0] <= hitbox.x+hitbox.width and event.pos[1] <= hitbox.y+hitbox.height:
							currentSelectedText = i
							break
					print(event)
				if event.type == QUIT:
					doit = False
				if event.type == KEYDOWN:
					if event.key == pygame.K_UP:
						currentSelectedText -= 1
					if event.key == pygame.K_DOWN:
						currentSelectedText += 1
					currentSelectedText %= shownChoices
					if event.key == pygame.K_RETURN:
						if currentSelectedText == 2:
							doAction = 1
							spriteIndex = 2
							textSans = 'Ta grosse daronne :).'
							textSansIndex = 0
						if currentSelectedText == 4:
							doAction = 1
							spriteIndex = spriteCount-1
							textSans = 'A plus le reuf !!'
							textSansIndex = 0
		pygame.display.update()
	pygame.display.quit()
	sys.exit()