from multiprocessing import freeze_support

from chess import Board

from chess_engine import ChessEngine
from genetic.fitnesses import checkmate, utility
from genetic.utility import chess_int_to_board
from genetic import FullBoard, Composer
from genetic.crossovers.singlepoint import SinglePoint
from genetic.mutations import random_forward_moves, add_random_piece

if __name__ == '__main__':
    freeze_support()

    engine = ChessEngine(5)

    # Testing composer
    max_fitness = 10.0
    crossover = SinglePoint()
    mutation = add_random_piece.AddRandomPieces()
    fitness = checkmate.Checkmate()
    genetic = Composer(engine, crossover, mutation, fitness, max_fitness)

    population = genetic.run(30, 50)

    for c in population:
        if c.score > 0:
            board = chess_int_to_board(c.body)
            print(board.fen())
