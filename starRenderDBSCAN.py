import pygame
from pygame.math import Vector3
import pygame.display
import pygame.draw
import pygame.event
import pygame.key
import math
import random

#import dbscan for clustering also numpy
from sklearn.cluster import DBSCAN
import numpy as np


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


	#define star positions for dbscan
	star_positions = np.array([star[0] for star in stars])

	#DBSCAN parameters:
	epsilon = 0.5
	min_samples = 5

	#define colors for clusters
	colors = [(np.random.randint(100, 255), np.random.randint(100,255), np.random.randint(100,255)) for _ in range(100)]

	#DBSCAN variables:
	dbscan_activate = False
	dbscan_step = 0
	clusters = np.full(len(stars), -1) #all stars noise


	while True:
		#if window is closed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#end the program
				pygame.quit()
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					dbscan_activate = True
					dbscan_step = 0
					clusters = np.full(len(stars), -1) #reset clusters

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

		#perform dbscan steps if active
		if dbscan_activate and dbscan_step < len(star_positions):
			dbscan = DBSCAN( eps = epsilon, min_samples = min_samples)
			clusters[:dbscan_step+1] = dbscan.fit_predict(star_positions[:dbscan_step+1])
			dbscan_step += 1


		#for drawing all stars
		for i, (position, magnitude) in enumerate(stars):
			#rotate the field
			rotated = position.rotate_x(rotation_x).rotate_y(rotation_y)
			#perspective projection
			scale = 2000 / (4 - rotated.z) #adjust scale for zoom / viewpoint
			x = rotated.x * scale + width / 2
			y = -rotated.y * scale + height / 2
			
			#if position within valid display range
			if 0 <= x < width  and 0 <= y < height:
				#define size
				size = max(1, int(5 - magnitude))
				#if clusters are noise
				if clusters [i] == -1:
					#adjust color based on magnitude small 0-10 range
					color = int(255 * (1.0 - (magnitude / 10 ))) % 256
					color = (color, color, color)
				else: #adjust colors for clusters
					color = colors[clusters[i] % len(colors)]

			#draw star as circle
			pygame.draw.circle(screen, color, (int(x), int(y)), size)

		#display clusters info:
		font = pygame.font.Font(None, 36)
		text = font.render(f"Points processed: {dbscan_step} / {len(stars)}", True, (255, 255, 255))
		screen.blit(text, (10,10))
		text = font.render(f"Epsilon: {epsilon: .2f}", True, (255, 255, 255))
		screen.blit(text, (10,50))
		text = font.render("Press D to start DBSCAN", True, (255, 255, 255))
		screen.blit(text, (10,90))

		pygame.display.flip()
		clock.tick(30)

if __name__ == "__main__":
	main()
