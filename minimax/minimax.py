import chess
from result import Result
from functools import cache

CUTOFF = 5

tmp_sequence = []
best_sequence = [None for _ in range(CUTOFF)]

@cache
def is_forward(move: str, white: bool) -> bool:
    if int(move[1]) < int(move[3]):
        return True if white else False
    else:
        return False if white else True


def search(state: chess.Board) -> chess.Move:
    result: Result = max_value(state, None, 0, float('-inf'), float('inf'))
    return result.move


def max_value(state: chess.Board, move: chess.Move, depth: int, alpha: int, beta: int) -> Result:
    if state.outcome() or depth == CUTOFF:
        # TODO: handle board initial position is mate
        return Result(move, calculate_utility(state, depth))

    best_move: Result = Result(None, float('-inf'))

    legal_moves = list(state.legal_moves)
    legal_moves = sorted(legal_moves, key=lambda m: (
        not state.is_capture(m),
        not state.gives_check(m),
        not is_forward(str(m), True)
    ))

    for a in legal_moves:
        state2 = state.copy()
        state2.push(a)
        tmp_sequence.append(state.san(a))
        result: Result = min_value(state2, a, depth + 1, alpha, beta)
        tmp_sequence.pop()
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
    legal_moves = sorted(legal_moves, key=lambda m: (
        not state.is_capture(m),
        not state.gives_check(m),
        not is_forward(str(m), False)
    ))

    for a in legal_moves:
        state2 = state.copy()
        state2.push(a)
        tmp_sequence.append(state.san(a))
        result: Result = max_value(state2, a, depth + 1, alpha, beta)
        tmp_sequence.pop()
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
        global best_sequence
        if len(best_sequence) >= len(tmp_sequence):
            best_sequence = tmp_sequence.copy()
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
m3_loaded_1 = chess.Board("r1b1kb1r/pppp1ppp/5q2/4n3/3KP3/2N3PN/PPP4P/R1BQ1B1R b kq - 0 1")
m3_loaded_2 = chess.Board("r3k2r/ppp2Npp/1b5n/4p2b/2B1P2q/BQP2P2/P5PP/RN5K w kq - 1 0")
m3_loaded_3 = chess.Board("r1b3kr/ppp1Bp1p/1b6/n2P4/2p3q1/2Q2N2/P4PPP/RN2R1K1 w - - 1 0")

m2_1 = chess.Board("r2qkb1r/pp2nppp/3p4/2pNN1B1/2BnP3/3P4/PPP2PPP/R2bK2R w KQkq - 1 0")
m2_2 = chess.Board("4kb1r/p2n1ppp/4q3/4p1B1/4P3/1Q6/PPP2PPP/2KR4 w k - 1 0")
m2_3 = chess.Board("r1b2k1r/ppp1bppp/8/1B1Q4/5q2/2P5/PPP2PPP/R3R1K1 w - - 1 0")
m2_4 = chess.Board("5rkr/pp2Rp2/1b1p1Pb1/3P2Q1/2n3P1/2p5/P4P2/4R1K1 w - - 1 0")
m2_5 = chess.Board("1r1kr3/Nbppn1pp/1b6/8/6Q1/3B1P2/Pq3P1P/3RR1K1 w - - 1 0")
m2_6 = chess.Board("5rk1/1p1q2bp/p2pN1p1/2pP2Bn/2P3P1/1P6/P4QKP/5R2 w - - 1 0")
m2_7 = chess.Board("r1nk3r/2b2ppp/p3b3/3NN3/Q2P3q/B2B4/P4PPP/4R1K1 w - - 1 0")
m2_8 = chess.Board("r4br1/3b1kpp/1q1P4/1pp1RP1N/p7/6Q1/PPB3PP/2KR4 w - - 1 0")
m2_9 = chess.Board("r1b2k1r/ppppq3/5N1p/4P2Q/4PP2/1B6/PP5P/n2K2R1 w - - 1 0")

search(m3_loaded_3)
print(*best_sequence)