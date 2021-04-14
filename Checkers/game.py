import pygame

from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board

class Game():
    def __init__(self, display):
        self._init()
        self.display = display

    def update (self):
        self.board.draw(self.display)
        self.draw_valid_moves(self.possible_moves)  # draw possible moves of selected piece
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.possible_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:  # if a piece is selected
            result = self._move(row, col)
            if not result:
                # unselect piece if move cannot be made
                self.selected = None
                self.possible_moves = {}
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:  # if it is a movable piece
            self.selected = piece
            self.possible_moves = self.board.get_valid_moves(piece)  # updates shown moves
            return True

        return False

    def _move(self, row, col):
        if (row, col) in self.possible_moves:  # if the selected position is a possible move
            skipped = self.possible_moves[(row, col)]  # skipped is the path that is taken to get to certain spot
            self.board.remove(skipped)  # the whole path is cleared

            self.board.move(self.selected, row, col)  # move piece to end of path
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.display, BLUE, (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2),15)

    def change_turn(self):
        self.possible_moves = {}  # resets shown moves
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def no_valid_moves(self):
        return self.board.no_valid_move(self.turn)

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
