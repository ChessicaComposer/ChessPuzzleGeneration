from chess_engine import ChessEngine
from genetic.utility import chess_int_to_board
from genetic import FullBoard
import chess

# Test
engine = ChessEngine(5)

genetic = FullBoard(engine)
population, evaluations = genetic.run(20, 20)

for c in population:
    board = chess_int_to_board(c)
    print(board.fen())