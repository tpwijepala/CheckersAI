from logging import captureWarnings
import pygame
from Checkers.constants import RED, WHITE
from copy import deepcopy


def minimax(board, depth, alpha, beta, max_player, game):
    if depth == 0 or board.winner() != None:  # last move in depth
        # evaluates every possible move by both players for given depth
        # and gets value of each end position by calculating # of pieces
        color = WHITE if max_player else RED
        
        # quiesence search checks if there are any immediate captures available
        # and if so, evalutes the board after the these immediate captures
        return -quiescence_search(board, alpha, beta, color, game), board


    if max_player:  # maximizing value // white move
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(board, WHITE, game):  # all possible moves in current position
            eval = minimax(move, depth - 1, alpha, beta, False, game)[0]
            # eval is value of move that red would make (value that would minimize white's value)
            # beta is current best red move which will lead red to minimizing score
            # alpha is current best white move which leads to white to maximizing score

            maxEval = max(maxEval, eval)  # chooses move w/ highest eval for current position
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                # if red has lower beta value than current alpha val, there is no longer a need to run
                # since red will choose the move which leads to minimizing score while white chooses a betters score
                break
            if maxEval == eval:
                best_move = move  # if current eval is lowest, set move to current move

        return maxEval, best_move

    else:  # minimizing value // red move
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(board, RED, game):
            eval = minimax(move, depth - 1, alpha, beta, True, game)[0]
            # eval is value of move that white would make (value that would maximizes white's value)
            # alpha is current best white move which leads to white to maximizing score
            # beta is current best red move which will lead red to minimizing score

            minEval = min(minEval, eval)  # chooses move w/ lowest eval for current position
            beta = min(beta, eval)
            if beta <= alpha:
                # if reds finds a move w/ lower eval, white won't care, white will use the alpha move since it
                # will lead white to maximizing his score
                break
            if minEval == eval:
                best_move = move  # if current eval is lowest, set best red move to current move

        return minEval, best_move

def quiescence_search(board, alpha, beta, color, game):
    eval = board.evaluate()
    
    if beta <= eval:
        return beta
    if alpha < eval:
        alpha = eval
    
    for capture in get_all_captures(board, color, game):
        opposite_color = RED if color == WHITE else WHITE
        # Evaluate board after series of immediate captures are completed
        score = -(quiescence_search(capture, -beta, -alpha, opposite_color, game))
        
        if (beta <= score):
            return beta
        if (alpha < score):
            alpha = score
            
    return alpha
            

def simulate_move(piece, move, board, game, skip):
    # creating imaginary board to help ai figure out best/worst eval
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():  # each end position and spaces skipped
            temp_board = deepcopy(board)  # w/ deep copy you can edit one copy w/o affecting the other
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)  # new board setup after possible move
            moves.append(new_board)  # possible moves from new move

    return moves  # updated moves from new position

def get_all_captures(board, color, game):
    captures = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():  # each end position and spaces skipped
            if skip:
                temp_board = deepcopy(board)  # w/ deep copy you can edit one copy w/o affecting the other
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = simulate_move(temp_piece, move, temp_board, game, skip)  # new board setup after possible move
                captures.append(new_board)  # possible moves from new move

    return captures