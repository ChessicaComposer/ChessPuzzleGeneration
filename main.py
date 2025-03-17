from multiprocessing import freeze_support

from chess_engine import ChessEngine
from genetic.utility import chess_int_to_board
from genetic import FullBoard
from genetic.crossovers.singlepoint import SinglePoint

if __name__ == '__main__':
    freeze_support()

    # Test
    engine = ChessEngine(5)
    crossover = SinglePoint()
    genetic = FullBoard(engine, crossover)
    population = genetic.run(5, 20)

    for c in population:
        if c.score > 0:
            board = chess_int_to_board(c.body)
            print(board.fen())
