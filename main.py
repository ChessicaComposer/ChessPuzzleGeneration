from multiprocessing import freeze_support

from chess import Board

from chess_engine import ChessEngine
from genetic.fitnesses.checkmate import Checkmate
from genetic.utility import chess_int_to_board
from genetic import FullBoard
from genetic.crossovers.singlepoint import SinglePoint
from genetic.mutations.random_forward_moves import RandomForwardMoves

if __name__ == '__main__':
    freeze_support()

    engine = ChessEngine(5)

    crossover = SinglePoint()
    mutation = RandomForwardMoves()
    fitness = Checkmate()
    genetic = FullBoard(engine, crossover, mutation, fitness)

    population = genetic.run(5, 20)

    for c in population:
        if c.score > 0:
            board = chess_int_to_board(c.body)
            print(board.fen())
