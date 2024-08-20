import numpy as np
from sklearn.cluster import DBSCAN
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("DBSCAN Clustering in 3D")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Generate random 3D data
np.random.seed(42)
n_points = 300
X = np.random.randn(n_points, 3) * 0.5

# Create clusters
X[100:200, 0] += 2
X[200:, 0] += 4

# Apply DBSCAN
eps = 0.3
min_samples = 5
dbscan = DBSCAN(eps=eps, min_samples=min_samples)
clusters = dbscan.fit_predict(X)

# Function to project 3D points to 2D
def project_3d_to_2d(point, scale=100, offset_x=width//2, offset_y=height//2):
    x, y, z = point
    return int(x * scale + offset_x), int(y * scale + offset_y - z * scale * 0.5)

# Main game loop
clock = pygame.time.Clock()
rotation = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Rotate points
    rotation += 0.01
    rot_matrix = np.array([
        [np.cos(rotation), -np.sin(rotation), 0],
        [np.sin(rotation), np.cos(rotation), 0],
        [0, 0, 1]
    ])
    rotated_points = X @ rot_matrix.T

    # Draw points
    for point, cluster in zip(rotated_points, clusters):
        x, y = project_3d_to_2d(point)
        color = pygame.Color(0)
        color.hsva = (((cluster + 1) * 30) % 360, 100, 100, 100)
        pygame.draw.circle(screen, color, (x, y), 3)

    pygame.display.flip()
    clock.tick(30)
