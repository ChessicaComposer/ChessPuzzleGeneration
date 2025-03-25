from functools import cache

import chess
from chess import Board

from .pstables import get_table

count = 0


@cache
def move_is_forward(move: str, white: bool) -> bool:
    if int(move[1]) < int(move[3]):
        return True if white else False
    else:
        return False if white else True


def _flip(square: int) -> int:
    return square ^ 56


def evaluate_piece_square(board: Board) -> int:
    white = 0
    black = 0
    piece_map = board.piece_map()
    pieces = piece_map.items()
    for sq, piece in pieces:
        table = get_table(piece.piece_type)
        if piece.color == chess.WHITE:
            white += table[sq]
        else:
            black += table[_flip(sq)]
    return white - black
