import chess

PIECE_VALUES = {
    chess.KING: 0,
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9
}


def evaluate_position(board: chess.Board) -> int:
    evaluation: int = 0

    # Evaluate piece imbalance
    for piece in board.piece_map().items():
        p = piece[1]
        if p.color == chess.WHITE:
            evaluation += PIECE_VALUES[p.piece_type]
        else:
            evaluation -= PIECE_VALUES[p.piece_type]

    return evaluation


