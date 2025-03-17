from .crossover import Crossover
from .genetic import Genetic
from common.evaluator import Evaluator, EvaluatorResponse
from .utility import chess_board_to_int, chess_int_to_board
from random import randint
import chess
from .chromosome import IntBoard, Chromosome

class FullBoard(Genetic, Crossover):
    def __init__(self, evaluator: Evaluator = None, crossover: Crossover = None):
        super().__init__(evaluator, crossover)

    def _fitness(self, chromosome: IntBoard) -> IntBoard:
        if chromosome.evaluated:
            return chromosome
        board = chess_int_to_board(chromosome.body)
        chromosome.set_evaluated(True)
        if not board.is_valid():
            chromosome.set_score(-10)
            return chromosome
        evaluation: EvaluatorResponse = self.evaluator.run(board)
        if evaluation.has_mate:
            chromosome.set_score(10)
        return chromosome

    def _mutate(self, population: list[IntBoard]) -> list[IntBoard]:
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

    # Create population
    def _create_population(self, amount: int) -> list[IntBoard]:
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

    def _run_tournament(self, population: list[IntBoard]) -> list[IntBoard]:
        population.sort(key=lambda c: c.score)
        print(list(map(lambda c: c.score, population)))
        population = population[len(population) // 2:]
        return population

    def _stop_condition(self, generation) -> bool:
        return False
