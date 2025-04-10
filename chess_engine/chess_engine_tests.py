from .chess_engine import ChessEngine
import chess
import unittest


# Recall that ply = mx2 - 1, so m5 = ply 9.

class TestChessEnginePly5(unittest.TestCase):
    engine = ChessEngine(5)

    # Boards with mates
    # - Mates with few pieces, e.g. 1 queen or 2 rooks to mate
    m_simple = [
        chess.Board("1k6/8/2Q5/8/8/2K5/8/8 w - - 0 1"),     #m5
        chess.Board("1k6/8/2QK4/8/8/8/8/8 w - - 0 1"),      #m3
        chess.Board("8/2k5/5R2/4R3/8/8/8/3K4 w - - 0 1"),   #rm3
        chess.Board("8/k7/6RR/8/8/8/8/4K3 w - - 0 1"),      #rm2
    ]

    # - Mates in two
    m2 = [
        chess.Board("r2qkb1r/pp2nppp/3p4/2pNN1B1/2BnP3/3P4/PPP2PPP/R2bK2R w KQkq - 1 0"),
        chess.Board("4kb1r/p2n1ppp/4q3/4p1B1/4P3/1Q6/PPP2PPP/2KR4 w k - 1 0"),
        chess.Board("r1b2k1r/ppp1bppp/8/1B1Q4/5q2/2P5/PPP2PPP/R3R1K1 w - - 1 0"),
        chess.Board("5rkr/pp2Rp2/1b1p1Pb1/3P2Q1/2n3P1/2p5/P4P2/4R1K1 w - - 1 0"),
        chess.Board("1r1kr3/Nbppn1pp/1b6/8/6Q1/3B1P2/Pq3P1P/3RR1K1 w - - 1 0"),
        chess.Board("5rk1/1p1q2bp/p2pN1p1/2pP2Bn/2P3P1/1P6/P4QKP/5R2 w - - 1 0"),
        chess.Board("r1nk3r/2b2ppp/p3b3/3NN3/Q2P3q/B2B4/P4PPP/4R1K1 w - - 1 0"),
        chess.Board("r4br1/3b1kpp/1q1P4/1pp1RP1N/p7/6Q1/PPB3PP/2KR4 w - - 1 0"),
        chess.Board("r1b2k1r/ppppq3/5N1p/4P2Q/4PP2/1B6/PP5P/n2K2R1 w - - 1 0")
    ]

    # - Mates in 3 with a loaded board (many pieces present)
    m3_loaded = [
        chess.Board("b5k1/1q3p1p/3p2p1/6Q1/1p3N2/1Prn3P/2P3P1/5RK1 w - - 0 27"),
        chess.Board("r1b1kb1r/pppp1ppp/5q2/4n3/3KP3/2N3PN/PPP4P/R1BQ1B1R b kq - 0 1"),
        chess.Board("r3k2r/ppp2Npp/1b5n/4p2b/2B1P2q/BQP2P2/P5PP/RN5K w kq - 1 0"),
        chess.Board("r1b3kr/ppp1Bp1p/1b6/n2P4/2p3q1/2Q2N2/P4PPP/RN2R1K1 w - - 1 0")
    ]


    # TESTS
    # - run()

    def test_run_m_simple(self):
        for i in range(len(self.m_simple)):
            board = self.m_simple[i]
            res = self.engine.run(board)

            if i == 0:
                self.assertIsNot(True, res.has_mate)
            else:
                self.assertEqual(True, res.has_mate)

    def test_run_m2(self):
        for i in range(len(self.m2)):
            board = self.m2[i]
            res = self.engine.run(board)

            self.assertEqual(True, res.has_mate)

    def test_run_m3_loaded(self):
        for i in range(len(self.m3_loaded)):
            board = self.m3_loaded[i]
            res = self.engine.run(board)

        self.assertEqual(True, res.has_mate)
