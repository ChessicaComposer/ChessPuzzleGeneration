from multiprocessing import freeze_support

from chess_engine import ChessEngine
from genetic.fitnesses.checkmate import Checkmate
from genetic.utility import chess_int_to_board
from genetic import FullBoard
from genetic.crossovers.singlepoint import SinglePoint
from genetic.mutations.random_forward_moves import RandomForwardMoves
import time
if __name__ == '__main__':
    freeze_support()
    start = time.time()
    # Test
    engine = ChessEngine(5)
    crossover = SinglePoint()
    mutation = RandomForwardMoves()
    fitness = Checkmate()
    genetic = FullBoard(engine, crossover, mutation, fitness)
    # conditions of form [time_limit,generation_limit, evaluation_limit]
    conditions = (300, 50, 10)
    population = genetic.run(conditions, 20)

    for c in population:
        if c.score > 0:
            board = chess_int_to_board(c.body)
            print(board.fen())
    print(time.time() - start)