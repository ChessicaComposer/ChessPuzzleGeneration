from genetic import Genetic
from utility import chess_board_to_int
from random import randint
import chess

class FullBoard(Genetic):
    def __init__(self, evaluator=None):
        super().__init__(evaluator)
        self.evaluator = evaluator

    
    def __fitness(self, chromosome: list[int]) -> float:
        raise NotImplementedError()
    

    def __mutate(self, population: list[list[int]]) -> list[list[int]]:
        raise NotImplementedError()


    # Create population
    def __create_population(self, amount: int) -> list[list[int]]:
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
    

    def __run_tournament(self, population: list[list[int]], evaluations: list[float]) -> list[list[int]]:
        raise NotImplementedError()
        """ selection = list(zip(population, evaluations))
        selection.sort(key=lambda x: x[1])
        selection = selection[len(population)/2:]
        return selection """
    

    def __reproduce(self, population: list[list[int]]) -> list[list[int]]:
        raise NotImplementedError()
    
    
    def __stop_condition(self, generation) -> bool:
        raise NotImplementedError()
