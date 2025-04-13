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

        if evaluation.has_mate:
            board = chess.Board(evaluation.fen)
            for move in evaluation.moves.line:
                s, c = self._analyse_checks(board)
                checkers.update(s)
                checks_count += c
                board.push(move)
            k = self._analyse_kingkillers(board)
            kingkillers.update(k)

        return Features(checkers, checks_count, kingkillers)

    def _analyse_checks(self, board: chess.Board) -> tuple[set[int], int]:
        checkers = set()
        checks_count = 0
        if not board.is_checkmate():
            if board.turn is False and board.is_check():
                checks_count += 1
                checkers_squares = board.checkers()
                for square in checkers_squares:
                    piece = board.piece_type_at(square)
                    checkers.add(piece)
        return checkers, checks_count

    def _analyse_kingkillers(self, board: chess.Board) -> set[int]:
        killers = set()
        killers_squares = board.attackers(chess.WHITE, board.king(chess.BLACK))
        for square in killers_squares:
            piece = board.piece_type_at(square)
            killers.add(piece)
        return killers
