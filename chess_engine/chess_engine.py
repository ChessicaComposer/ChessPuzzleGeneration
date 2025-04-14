import chess
from .result import Result
from functools import cache
from common.evaluator import Evaluator, EvaluatorResponse, Line
from .utility import evaluate_position, evaluate_move_stack, PIECE_VALUES

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
        self.count = 0
        self.initial_board = None
        self.initial_eval = 0
        self.moves = [None for _ in range(cutoff)]

    @cache
    def __is_forward(self, move: str, white: bool) -> bool:
        if int(move[1]) < int(move[3]):
            return True if white else False
        else:
            return False if white else True

    def run(self, board: chess.Board) -> EvaluatorResponse:
        if not board.is_valid():
            raise ValueError("Invalid chess board")

        self.initial_board = board.copy()

        # Sort moves for pre-search
        legal_moves = list(board.legal_moves)
        legal_moves = filter(lambda m: (
            board.gives_check(m),
        ), legal_moves)
        # Do a pre-search to find a mate in one (saves about 2 seconds if a M1 exists)
        for move in legal_moves:
            # No checks means no mate in one
            if not board.gives_check(move):
                break
            board.push(move)
            if board.is_checkmate():
                return EvaluatorResponse(board.fen(), board.is_checkmate(), self.__calculate_utility(board, 0), Line([move]))
            # Undo move
            board.pop()

        # If no move is found run negamax
        self.initial_eval = evaluate_position(board)

        line = Line([])
        res = self.negamax(board, float('-inf'), float('inf'), self.cutoff, line)
        # print(line.line)

        board_copy = board.copy()
        for move in line.line:
            board_copy.push(move)

        return EvaluatorResponse(board.fen(), board_copy.is_checkmate(), res, line)


    def negamax(self, state: chess.Board, alpha: int, beta: int, depth: int, pline: Line) -> int:
        line: Line = Line([])

        # If at max depth 0, calculate utility
        if depth == 0:
            return self.__calculate_utility(state, depth)

        best_value = float("-inf")

        # Find legal moves and use sorting heuristic to optimize alpha/beta pruning
        legal_moves = list(state.legal_moves)
        legal_moves = sorted(legal_moves, key=lambda m: (
            not state.is_capture(m),
            not state.gives_check(m),
        ))

        # Check if potential checkmate
        if len(legal_moves) == 0:
            pline.line = []
            return self.__calculate_utility(state, depth)

        for a in legal_moves:
            self.moves[depth - 1] = state.piece_at(a.to_square)
            state.push(a)
            score = -self.negamax(state, -beta, -alpha, depth - 1, line)
            state.pop()
            if score > best_value:
                best_value = score
                if score > alpha:
                    alpha = score
                    pline.line = [a] + line.line
            if score >= beta:
                return best_value
        return best_value

    def __calculate_utility(self, state: chess.Board, depth: int) -> int:
        # Utility must indicate a negative score, representing the badness of a position
        # for the given player
        if state.is_checkmate():
            return -(100000 + depth)
        evaluation = 0

        for i in range(self.cutoff - depth):
            piece = self.moves[i]
            if not piece:
                continue
            evaluation += PIECE_VALUES[piece.piece_type] * (-1 if piece.color == chess.WHITE else 1)
        return evaluation + self.initial_eval * (-1 if state.turn else 1)
