import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

#rgb
RED = (255, 0 , 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128,128,128)

BLUE = (0, 0, 255)

#king
CROWN = pygame.transform.scale(pygame.image.load('Checkers/assets/crown.png'),(45,25))