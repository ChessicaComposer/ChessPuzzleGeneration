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


mg_pawn_table = [
    0,   0,   0,   0,   0,   0,  0,   0,
    98, 134,  61,  95,  68, 126, 34, -11,
    -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
    0,   0,   0,   0,   0,   0,  0,   0,
]

eg_pawn_table = [
    0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
    94, 100,  85,  67,  56,  53,  82,  84,
    32,  24,  13,   5,  -2,   4,  17,  17,
    13,   9,  -3,  -7,  -7,  -8,   3,  -1,
    4,   7,  -6,   1,   0,  -5,  -1,  -8,
    13,   8,   8,  10,  13,   0,   2,  -7,
    0,   0,   0,   0,   0,   0,   0,   0,
]
mg_knight_table = [
    -167, -89, -34, -49,  61, -97, -15, -107,
    -73, -41,  72,  36,  23,  62,   7,  -17,
    -47,  60,  37,  65,  84, 129,  73,   44,
    -9,  17,  19,  53,  37,  69,  18,   22,
    -13,   4,  16,  13,  28,  19,  21,   -8,
    -23,  -9,  12,  10,  19,  17,  25,  -16,
    -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
]

eg_knight_table = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
]

mg_bishop_table = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
    -4,   5,  19,  50,  37,  37,   7,  -2,
    -6,  13,  13,  26,  34,  12,  10,   4,
    0,  15,  15,  15,  14,  27,  18,  10,
    4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
]

eg_bishop_table = [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
    -8,  -4,   7, -12, -3, -13,  -4, -14,
    2,  -8,   0,  -1, -2,   6,   0,   4,
    -3,   9,  12,   9, 14,  10,   3,   2,
    -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17,
]

mg_rook_table = [
    32,  42,  32,  51, 63,  9,  31,  43,
    27,  32,  58,  62, 80, 67,  26,  44,
    -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
]

eg_rook_table = [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
    7,  7,  7,  5,  4,  -3,  -5,  -3,
    4,  3, 13,  1,  2,   1,  -1,   2,
    3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20,
]

mg_queen_table = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
    -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
    -1, -18,  -9,  10, -15, -25, -31, -50,
]

eg_queen_table = [
    -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
    3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41,
]

mg_king_table = [
    -65,  23,  16, -15, -56, -34,   2,  13,
    29,  -1, -20,  -7,  -8,  -4, -38, -29,
    -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
    1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
]

eg_king_table = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
    10,  17,  23,  15,  20,  45,  44,  13,
    -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
]

PIECE_SQUARE_TABLES = {
    chess.PAWN:    (mg_pawn_table, eg_pawn_table),
    chess.KNIGHT:  (mg_knight_table, eg_knight_table),
    chess.BISHOP:  (mg_bishop_table, eg_bishop_table),
    chess.ROOK:    (mg_rook_table, eg_rook_table),
    chess.QUEEN:   (mg_queen_table, eg_queen_table),
    chess.KING:    (mg_king_table, eg_king_table),
}


def get_table(piece: int, end_game: bool = False) -> list[int]:
    return PIECE_SQUARE_TABLES[piece][1 if end_game else 0]


class Line:
    def __init__(self, cmove: int, line: list[chess.Move]):
        self.cmove = cmove
        self.line = line


class ChessEngine(Evaluator):
    def __init__(self, cutoff: int = 5):
        super().__init__()
        self.cutoff = cutoff
        self.count = 0

    @cache
    def __is_forward(self, move: str, white: bool) -> bool:
        if int(move[1]) < int(move[3]):
            return True if white else False
        else:
            return False if white else True

    def run(self, board: chess.Board) -> EvaluatorResponse:
        if not board.is_valid():
            raise ValueError("Invalid chess board")
        '''
        line = ["" for _ in range(self.cutoff)]
        res = self.__max_value(board, None, 0, float('-inf'), float('inf'), line)
        line = list(filter(lambda x: x != "", line))
        print(line)
        board_copy = board.copy()
        for move in line:
            board_copy.push(move)
        '''
        line = Line(0, [])
        res = self.negamax(board, float('-inf'), float('inf'), self.cutoff, line)
        #board_copy = board.copy()
        #for move in line.line:
        #    board_copy.push(move)
        print(str(self.count), "nodes")
        print(res)
        print(line.line)
        return EvaluatorResponse(board.is_checkmate(), 0)

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


    def negamax(self, state: chess.Board, alpha: int, beta: int, depth: int, pline: Line) -> int:
        line: Line = Line(0, [])
        self.count += 1
        if depth == 0:
            pline.cmove = 0
            return self.__calculate_utility(state, depth)
        best_value = float("-inf")
        legal_moves = list(state.legal_moves)
        legal_moves = sorted(legal_moves, key=lambda m: (
            not state.is_capture(m),
            not state.gives_check(m),
        ))
        if len(legal_moves) == 0:
            return self.__calculate_utility(state, depth)
        for a in legal_moves:
            state.push(a)
            score = -self.negamax(state, -beta, -alpha, depth - 1, line)
            state.pop()
            if score > best_value:
                best_value = score
                if score > alpha:
                    alpha = score
                    pline.line = [a] + line.line
                    pline.cmove = line.cmove + 1
            if score >= beta:
                return best_value
        return best_value

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
        white = 0
        black = 0
        for piece in board.piece_map().items():
            p = piece[1]
            sq = piece[0]
            #table = get_table(p.piece_type)
            if p.color == chess.WHITE:
                evaluation += piece_values[p.piece_type]
                #white += table[sq]
            else:
                evaluation -= piece_values[p.piece_type]
                #black += table[_flip(sq)]

        return evaluation + (white - black)

    def __calculate_utility(self, state: chess.Board, depth: int) -> int:
        if state.is_checkmate():
            return -(100000 - depth)
        return self.__evaluate_position(state)
