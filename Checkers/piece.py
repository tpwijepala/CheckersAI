import pygame
from .constants import RED, WHITE, GRAY, SQUARE_SIZE, CROWN


class Piece:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.calc_pos()

    def calc_pos(self):
        self.x = (SQUARE_SIZE * self.col) + (SQUARE_SIZE // 2)
        self.y = (SQUARE_SIZE * self.row) + (SQUARE_SIZE // 2)

    def make_king(self):
        self.king = True

    def draw(self, display):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(display, GRAY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(display, self.color, (self.x, self.y), radius)

        # draw crown when piece becomes king
        if self.king:
            display.blit(CROWN, ((self.x - CROWN.get_width() // 2), (self.y - CROWN.get_height() // 2)))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
