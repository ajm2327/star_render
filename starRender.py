import pygame
from pygame.math import Vector3
import pygame.display
import pygame.draw
import pygame.event
import pygame.key
import math
import random


#this function is for parsing the data and treating it as a vector
def parse_data(filename):
	#empty star dataset
	stars = []
	#reading the file
	with open(filename, 'r') as file:
		for line in file:
			#read the file line by line
			parts = line.split()
			if len(parts) >= 6:
				#define coords for every 3 datapoints
				x, y, z = map(float, parts[:3])
				#the 4th data point is the magnitude
				magnitude = float(parts[4])
				#add star to dataset
				stars.append((Vector3(x,y,z), magnitude))
	return stars



def main():
	#initialize pygame
	pygame.init()
	width, height = 1920, 1080
	display = (width, height)
	pygame.display.set_mode(display, pygame.DOUBLEBUF)
	
	#read star data
	stars = parse_data('stars.txt')

	#initialize clock
	clock = pygame.time.Clock()
	#define rotation axes
	rotation_x = 0
	rotation_y = 0
	
	while True:
		#if window is closed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#end the program
				pygame.quit()
				return
		#for rotating the render
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			rotation_y -= 0.03
		if keys[pygame.K_RIGHT]:
			rotation_y += 0.03
		if keys[pygame.K_UP]:
			rotation_x -= 0.03
		if keys[pygame.K_DOWN]:
			rotation_x += 0.03

		#define display
		screen = pygame.display.get_surface()
		#black background
		screen.fill((0,0,0))
		#for all stars
		for position, magnitude in stars:
			#rotate the field
			rotated = position.rotate_x(rotation_x).rotate_y(rotation_y)
			#perspective projection
			scale = 2000 / (4 - rotated.z) #adjust scale for zoom / viewpoint
			x = rotated.x * scale + width / 2
			y = -rotated.y * scale + height / 2
			
			#if position within valid display range
			if 0 <= x < width  and 0 <= y < height:
				#adjust color based on magnitude small 0-10 range
				color = int(255 * (1.0 - (magnitude / 10 ))) % 255
			#adjust size based on magnitude:
			size = max(1, int(5 - magnitude))

			#draw star as circle
			pygame.draw.circle(screen, (color, color, color), (int(x), int(y)), size)

		pygame.display.flip()
		clock.tick(60)

if __name__ == "__main__":
	main()
