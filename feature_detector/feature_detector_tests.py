from chess import QUEEN

from chess_engine import ChessEngine
from feature_detector import FeatureDetector, Features
import chess
import unittest

class TestFeatureDetectorPly5(unittest.TestCase):
    fd = FeatureDetector()
    boards = [
        chess.Board("4q3/8/QKR4R/4k3/8/8/b7/8 w - - 0 1"),
        chess.Board("3r4/pR2N3/2pkb3/5p2/8/2B5/qP3PPP/4R1K1 w - - 1 0")
    ]

    evaluations = []
    for board in boards:
        e = ChessEngine(5).run(board)
        evaluations.append(e)

    def test_run_kingkiller_queen(self):
        feats: Features = self.fd.run(self.evaluations[0])
        self.assertEqual({chess.ROOK, chess.QUEEN}, feats.checkers)
        self.assertEqual(2, feats.check_count)
        self.assertEqual({chess.QUEEN}, feats.kingkillers)

    def test_run_kingkiller_pawn(self):
        feats: Features = self.fd.run(self.evaluations[1])
        self.assertEqual({chess.BISHOP, chess.ROOK}, feats.checkers)
        self.assertEqual(2, feats.check_count)
        self.assertEqual({chess.PAWN}, feats.kingkillers)


"""
    def test_find_checkers(self):
        checkers = self.fd.get_checkers(self.evaluation)
        self.assertSetEqual({4, 5}, checkers)

    def test_find_kingkillers(self):
        killers = self.fd.get_kingkillers(self.evaluation)
        self.assertSetEqual({5}, killers)

    def test_set_checkers_killers(self):
        self.fd.run(self.evaluation)
        self.assertSetEqual({5}, self.fd.kingkillers)
        self.assertSetEqual({4, 5}, self.fd.checkers)
"""
