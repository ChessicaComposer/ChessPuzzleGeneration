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
    res = engine.run(Board("4kb1r/p2n1ppp/4q3/4p1B1/4P3/1Q6/PPP2PPP/2KR4 w k - 1 0"))
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