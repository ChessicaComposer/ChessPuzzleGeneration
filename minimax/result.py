import chess

class Result(object):
    def __init__(self, move: chess.Move, value: int):
        self.move = move
        self.value = value