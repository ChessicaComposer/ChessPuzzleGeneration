import chess
from constants import PIECE_MAP

def chess_board_to_int(board: chess.Board) -> list[int]:
    board_representation = [0 for _ in range(64)]

    for pos in board.piece_map().keys():
        board_representation[pos] = PIECE_MAP[str(board.piece_map()[pos])]