from multiprocessing import freeze_support

from chess_engine import ChessEngine
from genetic.utility import chess_int_to_board
from genetic import FullBoard

if __name__ == '__main__':
    freeze_support()

    # Test
    engine = ChessEngine(5)

    genetic = FullBoard(engine)
    population, evaluations = genetic.run(5, 20)

    for i, c in enumerate(population):
        if evaluations[i - 1] > 0:
            board = chess_int_to_board(c)
            print(board.fen())
