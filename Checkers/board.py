import pygame
from .constants import RED, WHITE, BLACK
from .constants import ROWS, COLS, SQUARE_SIZE
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_remaining = self.white_remaining = 12
        self.red_kings = self.white_kings = 0

        self.create_board()

    # layout for board
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_squares(self, display):
        display.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(display, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # evaluation for ai decision making
    def evaluate(self):
        # normal pieces are worth 1, kings are worth 1.5
        return self.white_remaining - self.red_remaining + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        # moves piece's position to empty spot & empty spot to position's spot
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)  # updates piece's variables

        if not piece.king:
            if row == ROWS - 1 or row == 0:
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def draw(self, display):
        self.draw_squares(display)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(display)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_remaining -= 1
                else:
                    self.white_remaining -= 1

    # checks if won via no pieces left
    def winner(self):
        if self.red_remaining <= 0:
            return str("WHITE")
        elif self.white_remaining <= 0:
            return str("RED")

        return None

    # checks if won via no valid moves
    def no_valid_move(self, col):
        moves = 0
        for piece in self.get_all_pieces(col):
            for move in self.get_valid_moves(piece):
                moves += 1

        # if no moves
        if moves < 1:
            return None
        else:
            return col

    def get_valid_moves(self, piece):
        moves = {}  # ([([position:piece/space]) , ([position,piece/space], & etc)]) & etc
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:  # move upwards
            # max makes piece look 2 rows above and stops from looking above of board
            moves.update(self._move_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._move_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.king:  # move downwards
            # min makes piece look 2 rows below and stops from looking below of board
            moves.update(self._move_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._move_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _move_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last_skipped = []
        for row in range(start, stop, step):  # loop checking possible moves in each row
            if left < 0:  # stop from looking outside the boards
                break

            position = self.board[row][left]  # position we are checking
            if position == 0:  # if the position is empty
                if skipped and not last_skipped:
                    # if we have already skipped but there isn't anything to skip currently
                    break

                elif skipped:  # double jumps
                    moves[(row, left)] = last_skipped + skipped  # update the moves to add the extra jump
                else:
                    moves[(row, left)] = last_skipped  # if no skip, we just move to the empty square

                if last_skipped:  # if we skipped over a opposite color piece
                    # update max row//stop
                    if step == -1:
                        rStop = max(row - 3, -1)
                    elif step == 1:
                        rStop = min(row + 3, ROWS)

                    # now use recursion to see if we can double jump
                    moves.update(self._move_left(row + step, rStop, step, color, left - 1, skipped=last_skipped))
                    moves.update(self._move_right(row + step, rStop, step, color, left + 1, skipped=last_skipped))
                break

            elif position.color == color:  # if position has a same colored piece
                break
            else:
                last_skipped = [position]

            left -= 1

        return moves

    def _move_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last_skipped = []
        for row in range(start, stop, step): # loop checking possible moves in each row
            if right >= COLS:
                break

            position = self.board[row][right]  # position we are checking
            if position == 0:  # stop from looking outside the boards
                if skipped and not last_skipped:
                    # if we have already skipped but there isn't anything to skip currently
                    break

                elif skipped:  # double jumps
                    moves[(row, right)] = last_skipped + skipped  # update the moves to add the extra jump
                else:
                    moves[(row, right)] = last_skipped # if no skip, we just move to the empty square

                if last_skipped:  # if we skipped over a opposite color piece
                    # update max row//stop
                    if step == -1:
                        rStop = max(row - 3, -1)
                    else:
                        rStop = min(row + 3, ROWS)

                    # now use recursion to see if we can double jump
                    moves.update(self._move_left(row + step, rStop, step, color, right - 1, skipped=last_skipped))
                    moves.update(self._move_right(row + step, rStop, step, color, right + 1, skipped=last_skipped))
                break

            elif position.color == color: # if position has a same colored piece
                break
            else:
                last_skipped = [position]

            right += 1

        return moves
