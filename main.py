from multiprocessing import freeze_support
from common.conditions import Conditions
from genetic import Composer
from genetic.utility import chess_int_to_board

if __name__ == '__main__':
    freeze_support()
    genetic = Composer(5)
    conditions = Conditions(None,50,10)
    result = genetic.run(40, 30)

    for c in result:
        board = chess_int_to_board(c.body)
        print(board.fen())
