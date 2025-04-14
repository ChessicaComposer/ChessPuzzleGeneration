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
    white = 0
    black = 0
    for piece in board.piece_map().items():
        p = piece[1]
        if p.color == chess.WHITE:
            evaluation += PIECE_VALUES[p.piece_type]
        else:
            evaluation -= PIECE_VALUES[p.piece_type]

    return evaluation


def evaluate_move_stack(board: chess.Board) -> int:
    _board = board.copy()
    evaluation: int = 0
    for _ in range(len(_board.move_stack)):
        move = _board.pop()
        piece = _board.piece_at(move.to_square)
        if piece:
            evaluation += PIECE_VALUES[piece.piece_type] * (-1 if piece.color == chess.WHITE else 1)
    return evaluation
