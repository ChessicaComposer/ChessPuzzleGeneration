from chess_engine import ChessEngine
from feature_detector import FeatureDetector, Features
import chess
import unittest

class TestFeatureDetectorPly5(unittest.TestCase):
    fd = FeatureDetector()
    board = chess.Board("4q3/8/QKR4R/4k3/8/8/b7/8 w - - 0 1")
    evaluation = ChessEngine(5).run(board)
    # evaluation.print()

    def test_run(self):
        feats: Features = self.fd.run(self.evaluation)
        self.assertEqual({4, 5}, feats.checkers)
        self.assertEqual(2, feats.check_count)
        self.assertEqual({5}, feats.kingkillers)
        # feats.print()


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
