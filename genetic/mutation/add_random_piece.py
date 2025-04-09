from genetic.mutation.base import Mutation
from random import randint
from ..constants import PIECE_MAP
from ..chromosome import IntBoard


class AddRandomPieces(Mutation):
    def __init__(self):
        super().__init__()

    def mutate(self, population: list[IntBoard]) -> list[IntBoard]:
        for i, chromosome in enumerate(population):
            if randint(0, 100) < 20:
                population[i].set_evaluated(False)
                board = population[i].body
                population[i].body = self._add_random_piece(board)
                # TODO: Randomly move pieces as well here

        return population

    def _add_random_piece(self, board: list[int]) -> list[int]:
        if not 0 in board:
            return board

        random_piece = randint(1, len(PIECE_MAP.keys()))

        # Generate a random piece until not invalid or a king
        while random_piece in [9, 10]:
            random_piece = randint(1, len(PIECE_MAP.keys()))

        random_position = randint(0, len(board) - 1)
        while board[random_position] in PIECE_MAP.values():
            random_position = randint(0, len(board) - 1)

        board[random_position] = random_piece
        return board
