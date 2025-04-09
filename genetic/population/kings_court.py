from random import randint

import chess
from .base import Population
from ..chromosome import IntBoard
from ..utility import chess_board_to_int

class KingsCourt(Population):
    def create(self, amount: int) -> list[IntBoard]:
        boards = [chess.Board("8/8/8/8/8/8/8/8 w HAha - 0 1") for _ in range(amount)]
        population: list[IntBoard] = []

        for board in boards:
            board_int = chess_board_to_int(board)

            # Place kings
            board_int[randint(0, len(board_int) - 1)] = 9
            board_int[randint(0, len(board_int) - 1)] = 10

            chromosome = IntBoard(board_int)

            population.append(chromosome)

        return population
