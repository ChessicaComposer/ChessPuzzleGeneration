from chess_engine import ChessEngine
from genetic import FullBoard
from genetic.utility import chess_int_to_board, chess_board_to_int
import chess

# Test
engine = ChessEngine(5)
test_board = chess.Board("r3k2r/ppp2Npp/1b5n/4p2b/2B1P2q/BQP2P2/P5PP/RN5K w kq - 1 0")
res = engine.run(test_board)

genetic = FullBoard(engine)
genetic.run(5, 10)