from chess_engine import ChessEngine
from genetic import FullBoard
from genetic.utility import chess_int_to_board, chess_board_to_int
import chess

# Test
engine = ChessEngine(5)
test_board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
res = engine.run(test_board)

#genetic = FullBoard(engine)
#genetic.run(5, 10)