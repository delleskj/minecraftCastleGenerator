from unittest import result
import pygame
from docutils.nodes import sidebar

from rectangleSplitter import RectangleSplitter
from pygame.locals import *

def debug_function():

	# initialize pygame
	pygame.init()
	clock = pygame.time.Clock()

	# Define the dimensions of screen object
	screen = pygame.display.set_mode((1000, 1000))

	tileNumber = 100
	splitter = RectangleSplitter(tileNumber, tileNumber)
	screenFactor = 1000 / tileNumber
	partitions = 10
	result = splitter._groundMatrix

	# Variable to keep our game loop running
	gameOn = True
	cooldown = 0
	currentCount = 1


	def update(deltaTime):
		global currentCount, cooldown, result
		if(currentCount <= partitions):
			cooldown += deltaTime
			if(cooldown > 300):
				cooldown = 0
				splitter.CalculatePartition(currentCount)
				result = splitter._groundMatrix
				currentCount += 1


	def draw():
		global result
		for ix, x in enumerate(result):
			for iz, z in enumerate(x):
				tmp_color = ((z / (float(partitions)) * 255), 0, 0)
				rect = pygame.Rect(ix*screenFactor, iz*screenFactor, screenFactor, screenFactor)
				pygame.draw.rect(screen, tmp_color, rect)


	# Our game loop
	while gameOn:
		dt = clock.tick(60)
		# for loop through the event queue
		for event in pygame.event.get():

			# Check for KEYDOWN event
			if event.type == KEYDOWN:

				# If the Backspace key has been pressed set
				# running to false to exit the main loop
				if event.key == K_SPACE:
					gameOn = False

			# Check for QUIT event
			elif event.type == QUIT:
				gameOn = False
		update(dt)
		draw()

		# Update the display using flip
		pygame.display.flip()

