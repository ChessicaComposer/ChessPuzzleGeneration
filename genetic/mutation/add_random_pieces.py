from genetic.mutation.base import Mutation
from random import random, randint
from ..constants import PIECE_MAP
from ..chromosome import IntBoard


class AddRandomPieces(Mutation):
    def __init__(self):
        super().__init__()
        self.chance = 0.25

    def mutate(self, population: list[IntBoard]) -> list[IntBoard]:
        for i, chromosome in enumerate(population):
            if random() < self.chance:
                population[i].set_evaluated(False)
                board = population[i].body

                if random() < 0.5:
                    population[i].body = self._add_random_piece(board)
                else:
                    population[i].body = self._make_random_moves(board)
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

    def _make_random_moves(self, board: list[int]) -> list[int]:
        piece_positions = []
        for i in range(len(board)):
            if board[i] != 0:
                piece_positions.append(i)

        if len(piece_positions) == 0:
            return board

        random_piece_pos = randint(0, len(piece_positions) - 1)
        random_pos = randint(0, len(board) - 1)

        if board[random_pos] != 0:
            old_piece = board[random_pos]
            board[random_pos] = board[random_piece_pos]
            board[random_piece_pos] = old_piece
        return board

    def _remove_random_piece(self, board: list[int]) -> list[int]:
        piece_positions = []
        for i in range(len(board)):
            if board[i] != 0:
                piece_positions.append(i)

        random_piece = piece_positions[randint(0, len(piece_positions) - 1)]
        while random_piece in [9, 10] and len(piece_positions) > 2:
            random_piece = piece_positions[randint(0, len(piece_positions) - 1)]

        board[random_piece] = 0
        return board
