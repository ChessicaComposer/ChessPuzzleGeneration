from multiprocessing import freeze_support
from chess_engine.chess_engine import ChessEngine
import chess
from common.conditions import Conditions
from genetic import Composer
from genetic import FullBoard
from genetic.utility import chess_int_to_board

if __name__ == '__main__':
    freeze_support()
    genetic = FullBoard(5)
    # Conditions of the form: Time, Generation, Evaluation limit
    conditions = Conditions(None,20,None)
    result = genetic.run(1, conditions)

    for c in result:
        board = chess_int_to_board(c.body)
        print(board.fen())
