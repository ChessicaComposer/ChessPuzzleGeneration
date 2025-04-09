from .crossover import Crossover
from .mutation import Mutation
from .fitness import Fitness
from .genetic import Genetic
from common.evaluator import Evaluator, EvaluatorResponse
from .utility import chess_board_to_int, chess_int_to_board
from random import randint
import chess
from .chromosome import IntBoard

class Composer(Genetic, Crossover, Fitness):
    def __init__(self, evaluator: Evaluator = None, crossover: Crossover = None, mutation: Mutation = None,
                 fitness: Fitness = None, max_fitness: float = 10.0):
        super().__init__(evaluator, crossover, mutation, fitness, max_fitness)

    # Create population
    def _create_population(self, amount: int) -> list[IntBoard]:
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

    def _run_tournament(self, population: list[IntBoard]) -> list[IntBoard]:
        population.sort(key=lambda c: c.score)
        print(list(map(lambda c: c.score, population)))
        population = population[len(population) // 2:]
        return population

    def _stop_condition(self, generation) -> bool:
        return False
