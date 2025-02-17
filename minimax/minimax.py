import chess
from result import Result

CUTOFF = 5

def search(state: chess.Board) -> chess.Move:
    result: Result = max_value(state, None, 0, float('-inf'), float('inf'))
    return result.move

def max_value(state: chess.Board, move: chess.Move, depth: int, alpha: int, beta: int) -> Result:
    if state.outcome() or depth == CUTOFF:
        # TODO: handle board initial position is mate
        return Result(move, calculate_utility(state, depth))

    best_move: Result = Result(None, float('-inf'))

    legal_moves = list(state.legal_moves)
    legal_moves.sort(key=lambda a: state.gives_check(a))

    for a in legal_moves:
        state2 = state.copy()
        state2.push(a)
        result: Result = min_value(state2, a, depth + 1, alpha, beta)
        if result.value > best_move.value:
            best_move.value = result.value
            best_move.move = a
            alpha = max(best_move.value, alpha)
        if best_move.value >= beta:
            return best_move
    return best_move

def min_value(state: chess.Board, move: chess.Move, depth: int, alpha: int, beta: int) -> Result:
    if state.outcome() or depth == CUTOFF:
        # TODO: handle board initial position is mate
        return Result(move, calculate_utility(state, depth))
    
    best_move: Result = Result(None, float('inf'))

    legal_moves = list(state.legal_moves)
    legal_moves.sort(key=lambda a: state.gives_check(a))

    for a in legal_moves:
        state2 = state.copy()
        state2.push(a)
        result: Result = max_value(state2, a, depth + 1, alpha, beta)
        if result.value < best_move.value:
            best_move.value = result.value
            best_move.move = a
            beta = min(best_move.value, beta)
        if best_move.value <= alpha:
            return best_move
    return best_move

def calculate_utility(state: chess.Board, depth: int) -> int:
    utility: int = 0
    if state.is_checkmate():
        utility = 1 + (CUTOFF - depth)
    else:
        utility = 0
    # if 0 black has made a move that turned game to checkmate (white is checking for this)
    if depth % 2 == 0:
        utility *= -1
    return utility 

# Boards with mates
m5 = chess.Board("1k6/8/2Q5/8/8/2K5/8/8 w - - 0 1")
m3 = chess.Board("1k6/8/2QK4/8/8/8/8/8 w - - 0 1")
rm3 = chess.Board("8/2k5/5R2/4R3/8/8/8/3K4 w - - 0 1")
rm2 = chess.Board("8/k7/6RR/8/8/8/8/4K3 w - - 0 1")
m3_loaded = chess.Board("b5k1/1q3p1p/3p2p1/6Q1/1p3N2/1Prn3P/2P3P1/5RK1 w - - 0 27")

# Current lazy way of printing mate sequence (Test for an existing sequence before calling if unsure)
def print_sequence(state: chess.Board):
    while (state.is_game_over() != True):
        move = search(state)
        print(state.san(move))
        state.push(move)
        global CUTOFF
        CUTOFF -= 1

print_sequence(m3_loaded)