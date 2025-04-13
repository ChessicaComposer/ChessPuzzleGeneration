from chess import QUEEN

from chess_engine import ChessEngine
from feature_detector import FeatureDetector, Features
import chess
import unittest

class TestFeatureDetectorPly5(unittest.TestCase):
    fd = FeatureDetector()
    board = chess.Board("4q3/8/QKR4R/4k3/8/8/b7/8 w - - 0 1")
    board0 = chess.Board("6Nn/2k5/4Q3/3P4/1K4R1/8/N7/8 w - - 0 1")
    evaluation = ChessEngine(5).run(board)
    evaluation0 = ChessEngine(5).run(board)
    # evaluation.print()

    def test_run(self):
        feats: Features = self.fd.run(self.evaluation)
        self.assertEqual({chess.ROOK, chess.QUEEN}, feats.checkers)
        self.assertEqual(2, feats.check_count)
        self.assertEqual({chess.QUEEN}, feats.kingkillers)
        # feats.print()

    def test_run0(self):
        feats: Features = self.fd.run(self.evaluation0)
        self.assertEqual({chess.ROOK}, feats.checkers)
        self.assertEqual(2, feats.check_count)
        self.assertEqual({chess.QUEEN}, feats.kingkillers)
        feats.print()


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
