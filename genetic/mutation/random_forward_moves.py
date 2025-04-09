from genetic.mutation.base import Mutation
from random import randint
from ..utility import chess_board_to_int, chess_int_to_board
from .. chromosome import IntBoard

class RandomForwardMoves(Mutation):
    def __init__(self):
        super().__init__()

    def mutate(self, population: list[IntBoard]) -> list[IntBoard]:
        for i in range(len(population) - 1):
            if randint(0, 100) < 20:
                population[i].set_evaluated(False)
                board = chess_int_to_board(population[i].body)
                for _ in range(randint(0, 10)):
                    legal_moves = board.legal_moves
                    if legal_moves is None or legal_moves.count() == 0:
                        break
                    board.push(list(legal_moves)[randint(0, legal_moves.count() - 1)])
                board = chess_board_to_int(board)
                population[i].body = board

        return population