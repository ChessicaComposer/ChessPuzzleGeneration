from multiprocessing import freeze_support
import time

from chess import Board

from chess_engine import ChessEngine
from genetic.utility import chess_int_to_board
from genetic import FullBoard

if __name__ == '__main__':
    freeze_support()

    # Test
    engine = ChessEngine(10)

    start = time.time()
    res = engine.run(Board("r2qkb1r/pp2nppp/3p4/2pNN1B1/2BnP3/3P4/PPP2PPP/R2bK2R w KQkq - 1 1"))
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