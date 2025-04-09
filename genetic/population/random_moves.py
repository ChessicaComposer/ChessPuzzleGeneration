from ..chromosome import IntBoard
from genetic.population.base import Population
import chess
from ..utility import chess_board_to_int
from random import randint

class RandomMoves(Population):
    def create(self, amount: int) -> list[IntBoard]:
        moves = 48
        boards = [chess.Board() for _ in range(amount)]
        population: list[IntBoard] = []

        for board in boards:
            for _ in range(moves):
                legal_moves = board.legal_moves
                if legal_moves.count() == 0:
                    break
                board.push(list(legal_moves)[randint(0, legal_moves.count() - 1)])

            board_int = chess_board_to_int(board)

            chromosome = IntBoard(board_int)

            population.append(chromosome)

        return population