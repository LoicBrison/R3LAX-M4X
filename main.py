import pygame
from pygame.locals import *
import sys
import time
import math
import threading

#import EmotionDetection.EmotionDetection

#from EmotionDetection import EmotionDetection

SCREEN_SIZE = (480, 320)
MARGIN_RATIO = 1/64.0
BORDER_SIZE = 3
X_MARGIN = SCREEN_SIZE[0]*MARGIN_RATIO
Y_MARGIN = SCREEN_SIZE[0]*MARGIN_RATIO

SANS_SPRITE_RECT = (0, 0, 36, 33)

SANS_TEXT_BOX = (0, SCREEN_SIZE[1]-(SCREEN_SIZE[1]/4), SCREEN_SIZE[0], SCREEN_SIZE[1]/4)

CHOICES = [
	"Salut toi !",
	"Qui est la ?",
	"Passe un message",
	"A plus !",
]

INITIAL_PROMPT = "Que veux tu faire ?"

SPRITE_INDICIES = [0, 1, 2, 4, 5, 6, 3]

if __name__ == '__main__':
	pygame.init()

	flags = pygame.NOFRAME | pygame.FULLSCREEN
	debug = False
	if len(sys.argv) > 1 and sys.argv[1].lower() == 'debug': debug = True
	if debug: flags &= ~pygame.FULLSCREEN

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
	textSansIndex = 0
	spriteIndex = 0

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

	arrowTimer = 0.0
	doAction = 0
	actionTimer = 0.0
	sleepingTimer = 0.0
	sleepTimer = 0.0
	goingToSleep = False

	tellingToPause = False
	tellingToPauseTimer = 0.0
	def resetSleep():
		global sleepingTimer
		global sleepTimer
		global goingToSleep
		global spriteIndex
		global tellingToPause
		sleepingTimer = 0.0
		sleepTimer = 0.0
		goingToSleep = False
		spriteIndex = 6 if tellingToPause else 0


	def speak(text):
		global textSans
		global textSansIndex
		textSans = text
		textSansIndex = 0


	context = [False, False, False, None, threading.Lock()]

	def the_func(context):
		t0 = None
		print("coucou")
		while not context[0]:
			if t0 is None or context[1] or (time.time_ns() - t0) / 1000000.0 > 1000.0*10:
				print("doing it")
				context[4].acquire()
				from time import sleep
				sleep(1)
				context[3] = 1
				context[2] = True
				context[4].release()
				t0 = time.time_ns()


	threadFunc = None
	if debug:
		threadFunc = the_func
	else:
		from EmotionDetection import EmotionDetection
		threadFunc = EmotionDetection.abc

	thread = threading.Thread(target=threadFunc, args=(context,))
	thread.start()



	while doit:
		t1 = time.time_ns()
		dt = float(t1 - t0)/1000000.0
		t0 = t1
		textTimer += dt
		arrowTimer += dt

		if not goingToSleep:
			sleepingTimer += dt

		if sleepingTimer > 5000.0:
			goingToSleep = True
			sleepingTimer = 0.0

		if goingToSleep: sleepTimer += dt

		if textSansIndex == len(textSans) and doAction == 1: doAction = 2
		if doAction == 2: actionTimer += dt

		if tellingToPause and textSansIndex == len(textSans): tellingToPauseTimer += dt
		if tellingToPauseTimer > 2000.0:
			tellingToPause = False
			tellingToPauseTimer = 0.0
			resetSleep()
			speak(INITIAL_PROMPT)

		if actionTimer > 1000.0:
			if currentSelectedText == 1:
				speak(INITIAL_PROMPT)
			elif currentSelectedText == 3:
				doit = False
			doAction = 0
			spriteIndex = 0
			actionTimer = 0

		if textTimer > 100.0:
			textTimer -= 100.0
			textSansIndex = min(textSansIndex+1, len(textSans))
			while len(textSans) > textSansIndex and textSans[textSansIndex].isspace():
				textSansIndex = min(textSansIndex + 1, len(textSans))

		if not tellingToPause and doAction == 0 and textSansIndex == len(textSans) and not context[4].locked() and context[3] is not None:
			resetSleep()
			context[4].acquire()
			if context[2]:
				context[2] = False
				if context[3] < 2:
					tellingToPause = True
					speak("Une petite pause ?")
					spriteIndex = 6

			context[4].release()


		if sleepTimer > 1250.0:
			sleepTimer -= 1250.0
			spriteIndex = min(spriteIndex+1, 4)



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
		surface.blit(spritesheet, (textBoxInner[0]+y, textBoxInner[1]+y), (SPRITE_INDICIES[spriteIndex] * SANS_SPRITE_RECT[2], SANS_SPRITE_RECT[1], SANS_SPRITE_RECT[2], SANS_SPRITE_RECT[3]))
		surface.blit(textSansImg, (textX, textBoxInner[1]+((textBoxInner[3]/2)-(textSansImg.get_height()/2))))
		if doAction == 0 and arrowTimer < 800.0:
			surface.blit(arrowLeft, (arrowX, arrowTopY + choicesBaseY + (textOffsetY * currentSelectedText)))
		if len(CHOICES) > fittingCount:
			surface.blit(arrowBottom, (((surface.get_width() - arrowBottom.get_width()) / 2, choiceY)))

		if doAction == 0:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					resetSleep()
					arrowTimer = 0.0
					for i, hitbox in enumerate(choicesHitBox):
						if event.pos[0] >= hitbox.x and event.pos[1] >= hitbox.y and event.pos[0] <= hitbox.x+hitbox.width and event.pos[1] <= hitbox.y+hitbox.height:
							currentSelectedText = i
							break
				if event.type == QUIT:
					doit = False
				if event.type == KEYDOWN:
					if event.key == pygame.K_UP:
						currentSelectedText -= 1
						resetSleep()
						arrowTimer = 0.0
					if event.key == pygame.K_DOWN:
						currentSelectedText += 1
						resetSleep()
						arrowTimer = 0.0
					currentSelectedText %= shownChoices
					if event.key == pygame.K_RETURN:
						resetSleep()
						arrowTimer = 0.0

						if currentSelectedText == 1:
							doAction = True
							spriteIndex = 5
							speak('Les autres.')
						if currentSelectedText == 3:
							doAction = True
							spriteIndex = 6
							speak('A plus tard !!')

		pygame.display.update()
	pygame.display.quit()
	context[0] = True
	if thread.is_alive(): thread.join()
	sys.exit()