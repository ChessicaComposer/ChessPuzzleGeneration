import chess
import chess.polyglot
from .result import Result
from functools import cache
from common.evaluator import Evaluator, EvaluatorResponse
from .utility import evaluate_position, PIECE_VALUES

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
class ttEntry:
    def __init__(self, score, depth, node_type, best_move):
        self.score = score
        self.depth = depth
        self.type = node_type
        self.valid = True
        self.move = best_move

class ChessEngine(Evaluator):
    def __init__(self, cutoff: int = 5):
        super().__init__()
        self.cutoff = cutoff
        self.count = 0
        self.initial_board = None
        self.initial_eval = 0
        self.removed_pieces = [None for _ in range(cutoff)]
        self.transposition_table = {}

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
                return EvaluatorResponse(board.fen(), board.is_checkmate(), self.__calculate_utility(board, 0), [move])
            # Undo move
            board.pop()

        # If no move is found run negamax
        self.initial_eval = evaluate_position(board)

        res = self.negamax(board, float('-inf'), float('inf'), self.cutoff)
        pv_line = self.__get_pvline(board)

        board_copy = board.copy()
        for move in pv_line:
            board_copy.push(move)
        return EvaluatorResponse(board.fen(), board_copy.is_checkmate(), res, pv_line)


    def negamax(self, state: chess.Board, alpha: int, beta: int, depth: int) -> int:
        # Save the initial alpha value to use determine the transposition table entry node type (beta is not needed to be stored as it does not get updated in negamax)
        alphaOrig = alpha

        # The transposition table is based roughly on the pseudocode in the following wiki: https://en.m.wikipedia.org/wiki/Negamax
        ## Check if state is in Transposition table
        hash_value = chess.polyglot.zobrist_hash(state)

        if hash_value in self.transposition_table:
            entry = self.transposition_table.get(hash_value)
            
            if entry.depth >= depth and entry.valid:
                # ALL-NODE
                if entry.type == 0:
                    beta = min(beta, entry.score)
                # CUT-NODE
                elif entry.type == 1:
                    alpha = max(alpha, entry.score)
                # PV-NODE
                elif entry.type == 2:
                    return entry.score
                
                if alpha >= beta:
                    return entry.score

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
            return self.__calculate_utility(state, depth)
        best_move = None
        for a in legal_moves:
            # This iterative evaluation will not take into account pawn promotions
            self.removed_pieces[depth - 1] = state.piece_at(a.to_square)
            state.push(a)
            score = -self.negamax(state, -beta, -alpha, depth - 1)
            state.pop()
            if score > best_value:
                best_value = score
                best_move = a
                if score > alpha:
                    alpha = score
            if score >= beta:
                break
    
        
        if best_value <= alphaOrig:
            # Set node type to All-node (Upper bound) (we call this 0)
            node_type = 0
        elif best_value >= beta:
            # Set node type to Cut-node (Lower bound) (we call this 1)
            node_type = 1
        else:  #alphaOrig < best_value < beta 
            # Set node type to PV (EXACT) (we call this 2)
            node_type = 2  
        old_entry = self.transposition_table.get(hash_value)
        if best_move is not None and (old_entry == None or old_entry.depth <= depth):
            entry = ttEntry(best_value, depth, node_type, best_move)
            self.transposition_table[hash_value] = entry
        return best_value

    def __calculate_utility(self, state: chess.Board, depth: int) -> int:
        # Utility must indicate a negative score, representing the badness of a position
        # for the given player
        if state.is_checkmate():
            return -(100000 + depth)
        evaluation = 0

        for i in range(self.cutoff - depth):
            piece = self.removed_pieces[i]
            if not piece:
                continue
            evaluation += PIECE_VALUES[piece.piece_type] * (-1 if piece.color == chess.WHITE else 1)
        return evaluation + self.initial_eval * (-1 if state.turn else 1)

    def __get_pvline(self, board: chess.Board) -> list[chess.Move]:
        board_copy = board.copy()
        pv = []
        for _ in range(self.cutoff):
            hash_value = chess.polyglot.zobrist_hash(board_copy)
            entry = self.transposition_table.get(hash_value)
            if entry is None or entry.move is None:
                break
            pv.append(entry.move)
            board_copy.push(entry.move)
        return pv
