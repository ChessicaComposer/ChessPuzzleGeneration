from chess_engine import ChessEngine
import chess

# Test
engine = ChessEngine(5)
test_board = chess.Board("r3k2r/ppp2Npp/1b5n/4p2b/2B1P2q/BQP2P2/P5PP/RN5K w kq - 1 0")
res = engine.run(test_board)