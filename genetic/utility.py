import chess
from .constants import PIECE_MAP

def chess_board_to_int(board: chess.Board) -> list[int]:
    board_representation = [0 for _ in range(64)]

    for pos in board.piece_map().keys():
        board_representation[pos] = PIECE_MAP[str(board.piece_map()[pos])]
    
    return board_representation

def chess_int_to_board(board: list[int]) -> chess.Board:
    board_representation = chess.Board("8/8/8/8/8/8/8/8")

    for pos, piece in enumerate(board):
        if piece == 0:
            continue
        piece_symbol = list(PIECE_MAP.keys())[piece - 1]
        piece = chess.Piece.from_symbol(piece_symbol)
        board_representation.set_piece_at(pos, piece)
    
    return board_representation
