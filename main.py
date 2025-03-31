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
    genetic = FullBoard(engine)
    population = genetic.run(5, 20)
    print(time.time()-start)
'''
    for c in population:
        if c.score > 0:
            board = chess_int_to_board(c.body)
            print(board.fen())
'''