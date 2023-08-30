import pygame
from Checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, RED
from Checkers.game import Game
from Checkers.board import Board
from Checkers.piece import Piece
from minimax.algorithm import minimax

FPS = 60

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers AI')


def mouse_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    playing = True
    frames = pygame.time.Clock()
    game = Game(DISPLAY)

    while playing:
        # run game at 60fps
        frames.tick(FPS)

        if game.winner() != None:
            print(game.winner() + " HAS WON THE GAME")
            break

        # checks if player can't make a move
        if game.no_valid_moves() == None:
            if game.turn == WHITE:
                print("WHITE HAS NO POSSIBLE MOVES")
            elif game.turn == RED:
                print("RED HAS NO POSSIBLE MOVES")
            break

        # white turn is ai's turn
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, float('-inf'), float('inf'), True, game)
            game.ai_move(new_board)

        # default pygame actions
        for action in pygame.event.get():

            # check if player quit game
            if action.type == pygame.QUIT:
                playing = False

            # gets mouse click position
            if action.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = mouse_pos(pos)
                game.select(row, col)

        # keeps updating game class
        game.update()
        
    pygame.quit()


main()
