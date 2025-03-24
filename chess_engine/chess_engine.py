import chess
from .result import Result
from functools import cache
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

    @cache
    def __is_forward(self, move: str, white: bool) -> bool:
        if int(move[1]) < int(move[3]):
            return True if white else False
        else:
            return False if white else True

    def run(self, board: chess.Board) -> EvaluatorResponse:
        if not board.is_valid():
            raise ValueError("Invalid chess board")
        line = ["" for _ in range(self.cutoff)]
        res = self.__max_value(board, None, 0, float('-inf'), float('inf'), line)
        line = list(filter(lambda x: x != "", line))
        print(line)
        board_copy = board.copy()
        for move in line:
            board_copy.push(move)
        return EvaluatorResponse(board_copy.is_checkmate(), res[1])

    def __max_value(self, state: chess.Board, move: chess.Move, depth: int, alpha: int, beta: int,
                    pline: list[str]) -> (chess.Move, int):
        if depth == self.cutoff:
            # TODO: handle board initial position is mate
            return move, self.__calculate_utility(state, depth)

        best_move: chess.Move = None
        best_score: int = float('-inf')

        legal_moves = list(state.legal_moves)

        if len(legal_moves) == 0:
            return move, self.__calculate_utility(state, depth)

        legal_moves = sorted(legal_moves, key=lambda m: (
            not state.is_capture(m),
            not state.gives_check(m),
            not self.__is_forward(str(m), True)
        ))

        for a in legal_moves:
            state.push(a)
            line = ["" for _ in range(self.cutoff)]
            result: (chess.Move, int) = self.__min_value(state, a, depth + 1, alpha, beta, line)
            state.pop()
            if result[1] > best_score:
                best_score = result[1]
                best_move = a
                if best_score > alpha:
                    alpha = best_score
                    pline[0] = best_move
                    for i in range(len(line) - 1):
                        pline[i + 1] = line[i]
            if best_score >= beta:
                return best_move, best_score
        return best_move, best_score

    def __min_value(self, state: chess.Board, move: chess.Move, depth: int, alpha: int, beta: int,
                    pline: list[str]) -> (chess.Move, int):
        if depth == self.cutoff:
            # TODO: handle board initial position is mate
            return move, self.__calculate_utility(state, depth)

        best_move: chess.Move = None
        best_score: int = float('inf')

        legal_moves = list(state.legal_moves)

        if len(legal_moves) == 0:
            return move, self.__calculate_utility(state, depth)

        legal_moves = sorted(legal_moves, key=lambda m: (
            not state.is_capture(m),
            not state.gives_check(m),
            not self.__is_forward(str(m), False)
        ))

        for a in legal_moves:
            state.push(a)
            line = ["" for _ in range(self.cutoff)]
            result: (chess.Move, int) = self.__max_value(state, a, depth + 1, alpha, beta, line)
            state.pop()
            if result[1] < best_score:
                best_score = result[1]
                best_move = a
                if best_score < beta:
                    beta = best_score
                    pline[0] = best_move
                    for i in range(len(line) - 1):
                        pline[i + 1] = line[i]
            if best_score <= alpha:
                return best_move, best_score
        return best_move, best_score

    # Domain specific chess position evaluation
    def __evaluate_position(self, board: chess.Board) -> int:
        evaluation: int = 0

        # Evaluate piece imbalance
        piece_values = {
            chess.KING   : 0,
            chess.PAWN   : 1,
            chess.KNIGHT : 3,
            chess.BISHOP : 3,
            chess.ROOK   : 5,
            chess.QUEEN  : 9
        }
        for piece in board.piece_map().values():
            if piece.color == chess.WHITE:
                evaluation += piece_values[piece.piece_type]
            else:
                evaluation -= piece_values[piece.piece_type]

        return evaluation

    def __calculate_utility(self, state: chess.Board, depth: int) -> int:
        if state.is_checkmate():
            return (1000 + (self.cutoff - depth)) * (-1 if state.turn else 1)
        return self.__evaluate_position(state)
