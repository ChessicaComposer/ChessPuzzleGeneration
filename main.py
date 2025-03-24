from multiprocessing import freeze_support
import time

from chess import Board

from chess_engine import ChessEngine
from genetic.utility import chess_int_to_board
from genetic import FullBoard

if __name__ == '__main__':
    freeze_support()

    # Test
    engine = ChessEngine(5)

    start = time.time()
    res = engine.run(Board("1k6/8/2QK4/8/8/8/8/8 w - - 0 1"))
    end = time.time()
    print(end - start)

    #genetic = FullBoard(engine)
    #population = genetic.run(5, 20)
'''
    for c in population:
        if c.score > 0:
            board = chess_int_to_board(c.body)
            print(board.fen())
'''