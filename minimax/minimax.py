import chess
from result import Result

def search(state: chess.Board) -> chess.Move:
    result: Result = max_value(state, None)
    return result.move

def max_value(state: chess.Board, move: chess.Move) -> Result:
    if state.is_checkmate:
        # TODO: handle board initial position is mate
        return Result(move, calculate_utility)

    best_move: Result = Result(None, float('-inf'))

    for a in state.legal_moves:
        state2 = state.copy()
        state2.push(a)
        result: Result = min_value(state2, a)
        if result.value > best_move.value:
            best_move.value = result.value
            best_move.move = a
    return best_move

def min_value(state: chess.Board, move: chess.Move) -> Result:
    if state.is_checkmate:
        # TODO: handle board initial position is mate
        return Result(move, calculate_utility)
    
    best_move: Result = Result(None, float('inf'))

    for a in state.legal_moves:
        state2 = state.copy()
        state2.push(a)
        result: Result = min_value(state2, a)
        if result.value < best_move.value:
            best_move.value = result.value
            best_move.move = a
    return best_move

def calculate_utility(state: chess.Board):
    return None

