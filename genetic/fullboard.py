from .genetic import Genetic
from common.evaluator import Evaluator, EvaluatorResponse
from .utility import chess_board_to_int, chess_int_to_board
from random import randint
import chess


class FullBoard(Genetic):
    def __init__(self, evaluator: Evaluator = None):
        super().__init__(evaluator)

    def _fitness(self, chromosome: list[int]) -> float:
        board = chess_int_to_board(chromosome)
        if not board.is_valid():
            return -10
        evaluation: EvaluatorResponse = self.evaluator.run(board)
        if evaluation.has_mate:
            return 10
        else:
            return 0

    def _mutate(self, population: list[list[int]]) -> list[list[int]]:
        for i in range(len(population)-1):
            if randint(0, 100) < 20:
                board = chess_int_to_board(population[i])
                for _ in range(randint(1, 10)):
                    legal_moves = board.legal_moves
                    board.push(list(legal_moves)[randint(0, legal_moves.count() - 1)])
                board = chess_board_to_int(board)
                population[i] = board

        return population

    # Create population
    def _create_population(self, amount: int) -> list[list[int]]:
        moves = 24
        boards = [chess.Board() for _ in range(amount)]
        population = []

        for board in boards:
            for _ in range(moves):
                legal_moves = board.legal_moves
                if legal_moves.count() == 0:
                    break
                board.push(list(legal_moves)[randint(0, legal_moves.count() - 1)])

            board_int = chess_board_to_int(board)

            population.append(board_int)

        return population

    def _run_tournament(self, population: list[list[int]], evaluations: list[float]) -> list[list[int]]:
        selection = list(zip(population, evaluations))
        selection.sort(key=lambda x: x[1])
        selection = selection[len(population)//2:]
        selection = list(map(lambda x: x[0], selection))
        return selection

    def _mate(self, parent1: list[int], parent2: list[int]) -> list[list[int]]:
        half = len(parent1) // 2
        return [parent1[:half] + parent2[half:], parent2[:half] + parent1[half:]]

    def _reproduce(self, population: list[list[int]]) -> list[list[int]]:
        offspring = []
        for i in range(0, len(population)-1, 2):
            children = self._mate(population[i], population[i+1])
            offspring += children
        if len(population) % 2 != 0:
            children = self._mate(population[0], population[-1])
            offspring.append(children[0])
        return offspring

    def _stop_condition(self, generation) -> bool:
        return False
