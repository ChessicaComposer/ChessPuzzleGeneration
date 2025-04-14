import chess
from common import EvaluatorResponse, Line


class Features:
    def __init__(self,
                 pieces: tuple[dict[int, int], dict[int, int]],
                 checkers: set[int],
                 checks_count: int,
                 king_attackers: set[int]
                 ):
        self._pieces_ = pieces
        self.checkers = checkers
        self.check_count = checks_count
        self.king_attackers = king_attackers

    def print(self):
        print(self._pieces_)
        print(self.checkers)
        print(self.check_count)
        print(self.king_attackers)

    def count_pieces(self, color: chess.Color):
        pieces: dict = self._pieces_[self._convert_color(color)]
        return sum(pieces.values())

    def count_piece_type(self, color: chess.Color, piece_type: chess.PieceType):
        pieces: dict = self._pieces_[self._convert_color(color)]
        return pieces[piece_type]

    def _convert_color(self, color: chess.Color) -> int:
        if color is chess.WHITE: return 1
        elif color is chess.BLACK: return 0
        else: raise ValueError


class FeatureDetector:
    def __init__(self):
        # Helper field
        self._last_evaluated_fen = None

    def run(self, evaluation: EvaluatorResponse) -> Features:
        # Auxiliary sets
        pieces = {}
        checkers = set()
        checks_count = 0
        king_attackers = set()

        if evaluation.has_mate:
            board = chess.Board(evaluation.fen)
            pieces = self._analyse_pieces(board)
            for move in evaluation.moves.line:
                s, c = self._analyse_checks(board)
                checkers.update(s)
                checks_count += c
                board.push(move)
            k = self._analyse_kingattackers(board)
            king_attackers.update(k)

        return Features(pieces, checkers, checks_count, king_attackers)

    def _analyse_pieces(self, board: chess.Board) -> tuple[dict[int, int], dict[int, int]]:
        black = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
        white = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
        for square in chess.SQUARES:
            if board.piece_at(square) is not None:
                if board.color_at(square) == chess.WHITE:
                    white[board.piece_type_at(square)] += 1
                else: black[board.piece_type_at(square)] += 1
        return black, white

    def _analyse_checks(self, board: chess.Board) -> tuple[set[int], int]:
        checkers = set()
        checks_count = 0
        if not board.is_checkmate():
            if board.turn is chess.BLACK and board.is_check():
                checks_count += 1
                checkers_squares = board.checkers()
                for square in checkers_squares:
                    piece = board.piece_type_at(square)
                    checkers.add(piece)
        return checkers, checks_count

    def _analyse_kingattackers(self, board: chess.Board) -> set[int]:
        attackers = set()
        attackers_squares = board.attackers(chess.WHITE, board.king(chess.BLACK))
        for square in attackers_squares:
            piece = board.piece_type_at(square)
            attackers.add(piece)
        return attackers