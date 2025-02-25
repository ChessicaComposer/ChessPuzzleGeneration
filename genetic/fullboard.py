from .genetic import Genetic
from common.evaluator import Evaluator, EvaluatorResponse
from .utility import chess_board_to_int
from random import randint
import chess

class FullBoard(Genetic):
    def __init__(self, evaluator: Evaluator=None):
        super().__init__(evaluator)

    
    def _fitness(self, chromosome: list[int]) -> float:
        raise NotImplementedError()
    

    def _mutate(self, population: list[list[int]]) -> list[list[int]]:
        raise NotImplementedError()


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
        raise NotImplementedError()
        """ selection = list(zip(population, evaluations))
        selection.sort(key=lambda x: x[1])
        selection = selection[len(population)/2:]
        return selection """
    

    def _reproduce(self, population: list[list[int]]) -> list[list[int]]:
        raise NotImplementedError()
    
    
    def _stop_condition(self, generation) -> bool:
        raise NotImplementedError()
