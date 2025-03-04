class Chromosome:
    # Abstract do not initialize
    def __init__(self, body: any):
        self.body = body
        self.score = 0.0
        self.evaluated: bool = False

    def set_score(self, score: float) -> None:
        self.score = score

    def set_evaluated(self, evaluated: bool) -> None:
        self.evaluated = evaluated


class IntBoard(Chromosome):
    def __init__(self, body: list[int]):
        super().__init__(body)
