import chess
from result import Result

CUTOFF = 3

best_mate = [None for _ in range(10)]

def search(state: chess.Board) -> chess.Move:
    result: Result = max_value(state, None, 0)
    return result.move

def max_value(state: chess.Board, move: chess.Move, depth: int) -> Result:
    if state.outcome() or depth == CUTOFF:
        # TODO: handle board initial position is mate
        return Result(move, calculate_utility(state, depth))

    best_move: Result = Result(None, float('-inf'))

    for a in state.legal_moves:
        state2 = state.copy()
        state2.push(a)
        result: Result = min_value(state2, a, depth + 1)
        if result.value > best_move.value:
            best_move.value = result.value
            best_move.move = a
    return best_move

def min_value(state: chess.Board, move: chess.Move, depth: int) -> Result:
    if state.outcome() or depth == CUTOFF:
        # TODO: handle board initial position is mate
        return Result(move, calculate_utility(state, depth))
    
    best_move: Result = Result(None, float('inf'))

    for a in state.legal_moves:
        state2 = state.copy()
        state2.push(a)
        result: Result = max_value(state2, a, depth + 1)
        if result.value < best_move.value:
            best_move.value = result.value
            best_move.move = a
    return best_move

def calculate_utility(state: chess.Board, depth: int):
    utility: float = 0
    if state.is_checkmate():
        utility = 1 + (CUTOFF - depth)
        global best_mate
        if len(state.move_stack) < len(best_mate):
            best_mate = state.move_stack
    else:
        utility = 0
    # if 0 black has made a move that turned game to checkmate (white is checking for this)
    if depth % 2 == 0:
        utility *= -1
    return utility 

# Mate in 1 position
m5 = chess.Board("1k6/8/2Q5/8/8/2K5/8/8 w - - 0 1")
m3 = chess.Board("1k6/8/2QK4/8/8/8/8/8 w - - 0 1")
rm3 = chess.Board("8/2k5/5R2/4R3/8/8/8/3K4 w - - 0 1")
rm2 = chess.Board("8/k7/6RR/8/8/8/8/4K3 w - - 0 1")


#print(search(rm2))
while (rm2.is_game_over() != True):
    move = search(rm2)
    print(move)
    rm2.push(move)
#print(best_mate)
