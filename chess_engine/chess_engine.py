import chess
from .result import Result
from functools import cache
from common.evaluator import Evaluator, EvaluatorResponse

class ChessEngine(Evaluator):
    def __init__(self, cutoff: int = 5):
        super().__init__()
        self.cutoff = cutoff
        self.__tmp_sequence = []
        self.__best_sequence = [None for _ in range(cutoff)]
        self.__has_mate = False

    @cache
    def __is_forward(self, move: str, white: bool) -> bool:
        if int(move[1]) < int(move[3]):
            return True if white else False
        else:
            return False if white else True
        
    def __reset(self):
        self.__tmp_sequence = []
        self.__best_sequence = [None for _ in range(self.cutoff)]
        self.__has_mate = False

    def run(self, board: chess.Board) -> EvaluatorResponse:
        self.__reset()
        self.__max_value(board, None, 0, float('-inf'), float('inf'))
        return EvaluatorResponse(self.__has_mate)


    def __max_value(self, state: chess.Board, move: chess.Move, depth: int, alpha: int, beta: int) -> Result:
        if state.outcome() or depth == self.cutoff:
            # TODO: handle board initial position is mate
            return Result(move, self.__calculate_utility(state, depth))

        best_move: Result = Result(None, float('-inf'))

        legal_moves = list(state.legal_moves)
        legal_moves = sorted(legal_moves, key=lambda m: (
            not state.is_capture(m),
            not state.gives_check(m),
            not self.__is_forward(str(m), True)
        ))

        for a in legal_moves:
            state2 = state.copy()
            state2.push(a)
            self.__tmp_sequence.append(state.san(a))
            result: Result = self.__min_value(state2, a, depth + 1, alpha, beta)
            self.__tmp_sequence.pop()
            if result.value > best_move.value:
                best_move.value = result.value
                best_move.move = a
                alpha = max(best_move.value, alpha)
            if best_move.value >= beta:
                return best_move
        return best_move


    def __min_value(self, state: chess.Board, move: chess.Move, depth: int, alpha: int, beta: int) -> Result:
        if state.outcome() or depth == self.cutoff:
            # TODO: handle board initial position is mate
            return Result(move, self.__calculate_utility(state, depth))

        best_move: Result = Result(None, float('inf'))

        legal_moves = list(state.legal_moves)
        legal_moves = sorted(legal_moves, key=lambda m: (
            not state.is_capture(m),
            not state.gives_check(m),
            not self.__is_forward(str(m), False)
        ))

        for a in legal_moves:
            state2 = state.copy()
            state2.push(a)
            self.__tmp_sequence.append(state.san(a))
            result: Result = self.__max_value(state2, a, depth + 1, alpha, beta)
            self.__tmp_sequence.pop()
            if result.value < best_move.value:
                best_move.value = result.value
                best_move.move = a
                beta = min(best_move.value, beta)
            if best_move.value <= alpha:
                return best_move
        return best_move


    def __calculate_utility(self, state: chess.Board, depth: int) -> int:
        utility: int = 0
        if state.is_checkmate():
            utility = 1 + (self.cutoff - depth)
            if len(self.__best_sequence) >= len(self.__tmp_sequence) and depth % 2 != 0:
                self.__best_sequence = self.__tmp_sequence.copy()
                self.__has_mate = True
        else:
            utility = 0
        # if 0 black has made a move that turned game to checkmate (white is checking for this)
        if depth % 2 == 0:
            utility *= -1
        return utility