import chess
from common import EvaluatorResponse, Line


class Features:
    def __init__(self,
                 checkers: set[int],
                 checks_count: int,
                 kingkillers: set[int]
                ):
        self.checkers = checkers
        self.check_count = checks_count
        self.kingkillers = kingkillers

    def print(self):
        print(self.checkers)
        print(self.check_count)
        print(self.kingkillers)


class FeatureDetector:
    def __init__(self):
        # Helper field
        self._last_evaluated_fen = None

    def run(self, evaluation: EvaluatorResponse) -> Features:
        # Auxiliary sets
        checkers = set()
        checks_count = 0
        kingkillers = set()

        board = chess.Board(evaluation.fen)
        for move in evaluation.moves.line:
            self._analyse_checks(checkers, checks_count, board)
            board.push(move)
        self._analyse_kingkillers(kingkillers, board)

        return Features(checkers, checks_count, kingkillers)

    def _analyse_checks(self, checkers: set[int], checks_count: int, board: chess.Board):
        if board.turn is False and board.is_check():
            checks_count += 1
            checkers_squares = board.checkers()
            for square in checkers_squares:
                piece = board.piece_type_at(square)
                checkers.add(piece)

    def _analyse_kingkillers(self, killers: set[int], board: chess.Board):
        killers_squares = board.attackers(chess.WHITE, board.king(False))
        for square in killers_squares:
            piece = board.piece_type_at(square)
            killers.add(piece)


"""
    def set_fields(self, checkers: set[int] | set, kingkillers: set[int] | set):
        self.checkers.clear()
        self.kingkillers.clear()
        self.checkers = checkers
        self.kingkillers = kingkillers

    def run(self, evaluation: EvaluatorResponse):
        checkers = set()
        killers = set()
        if evaluation.has_mate:
            board = chess.Board(evaluation.fen)
            for move in evaluation.moves.line:
                if board.turn is False and board.is_check():
                    checkers_squares = board.checkers()
                    for square in checkers_squares:
                        piece = board.piece_type_at(square)
                        checkers.add(piece)
                board.push(move)
            killers_squares = board.attackers(chess.WHITE, board.king(False))
            for square in killers_squares:
                piece = board.piece_type_at(square)
                killers.add(piece)
        self.set_fields(checkers, killers)

    # Checkers: The (white) pieces that checked the (black) king, incl. checkmate.
    def get_checkers(self, evaluation: EvaluatorResponse) -> set[int] | set:
        checkers = set()
        if evaluation.has_mate:
            board = chess.Board(evaluation.fen)
            for move in evaluation.moves.line:
                if board.turn is False and board.is_check():
                    checkers_squares = board.checkers()
                    for square in checkers_squares:
                        piece = board.piece_type_at(square)
                        checkers.add(piece)
                board.push(move)
        return checkers

    # Kingkillers: The last (white) piece(s) attacking the (black) king at checkmate
    def get_kingkillers(self, evaluation: EvaluatorResponse) -> set[int] | set:
        killers = set()
        if evaluation.has_mate:
            board = chess.Board(evaluation.fen)
            for move in evaluation.moves.line:
                board.push(move)
            killers_squares = board.attackers(chess.WHITE, board.king(False))
            for square in killers_squares:
                piece = board.piece_type_at(square)
                killers.add(piece)
        return killers
"""