import chess
from .result import Result
from .utility import *
from common.evaluator import Evaluator, EvaluatorResponse

"""
Sources

Minimax Algorithm and Alpha-Beta Pruning
Implementation based on Russel S. and Norvig P.
"Artificial Intelligence: A Modern Approach"
ISBN 13: 978-0-13-461099-3

Principle Variation Line used in max_value and min_value
Inspired by "PV-List on the Stack": https://www.chessprogramming.org/Principal_Variation#:~:text=The%20Principal%20variation%20(PV)%20is,the%20PV%20are%20PV%2Dnodes.
Author: Bruce Moreland 2001
Last modified: 11/04/02
"""


class ChessEngine(Evaluator):
    def __init__(self, cutoff: int = 5):
        super().__init__()
        self.cutoff = cutoff

    def run(self, board: chess.Board) -> EvaluatorResponse:
        if not board.is_valid():
            raise ValueError("Invalid chess board")
        line = ["" for _ in range(self.cutoff)]
        result = self.__max_value(board, None, 0, float('-inf'), float('inf'), line)
        line = list(filter(lambda x: x != "", line))
        board_copy = board.copy()
        for move in line:
            board_copy.push(move)
        return EvaluatorResponse(board_copy.is_checkmate(), result.value)

    def __max_value(self, state: chess.Board, move: chess.Move, depth: int, alpha: int, beta: int,
                    pline: list[str]) -> Result:
        if state.outcome() or depth == self.cutoff:
            # TODO: handle board initial position is mate
            return Result(move, self.__calculate_utility(state, depth))

        best_move: Result = Result(None, float('-inf'))

        legal_moves = list(state.legal_moves)
        legal_moves = sorted(legal_moves, key=lambda m: (
            not state.is_capture(m),
            not state.gives_check(m),
            not move_is_forward(str(m), True)
        ))

        for a in legal_moves:
            state2 = state.copy()
            state2.push(a)
            line = ["" for _ in range(self.cutoff)]
            result: Result = self.__min_value(state2, a, depth + 1, alpha, beta, line)
            if result.value > best_move.value:
                best_move.value = result.value
                best_move.move = a
                if best_move.value > alpha:
                    pline[0] = best_move.move
                    for i in range(len(line) - 1):
                        pline[i + 1] = line[i]
                alpha = max(best_move.value, alpha)
            if best_move.value >= beta:
                return best_move
        return best_move

    def __min_value(self, state: chess.Board, move: chess.Move, depth: int, alpha: int, beta: int,
                    pline: list[str]) -> Result:
        if state.outcome() or depth == self.cutoff:
            # TODO: handle board initial position is mate
            return Result(move, self.__calculate_utility(state, depth))

        best_move: Result = Result(None, float('inf'))

        legal_moves = list(state.legal_moves)
        legal_moves = sorted(legal_moves, key=lambda m: (
            not state.is_capture(m),
            not state.gives_check(m),
            not move_is_forward(str(m), False)
        ))

        for a in legal_moves:
            state2 = state.copy()
            state2.push(a)
            line = ["" for _ in range(self.cutoff)]
            result: Result = self.__max_value(state2, a, depth + 1, alpha, beta, line)
            if result.value < best_move.value:
                best_move.value = result.value
                best_move.move = a
                if best_move.value < beta:
                    pline[0] = best_move.move
                    for i in range(len(line) - 1):
                        pline[i + 1] = line[i]
                beta = min(best_move.value, beta)
            if best_move.value <= alpha:
                return best_move
        return best_move

    def __calculate_utility(self, state: chess.Board, depth: int) -> int:
        utility: int = 0
        if state.is_checkmate():
            utility = 1000 + (self.cutoff - depth)
            if depth % 2 == 0:
                utility *= -1
        else:
            utility = evaluate_piece_square(state)
        return utility
