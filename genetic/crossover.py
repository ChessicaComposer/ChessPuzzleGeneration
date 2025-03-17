from .chromosome import Chromosome

class Crossover:
    def __init__(self):
        pass

    def reproduce(self, population: list[Chromosome]) -> list[Chromosome]:
        raise NotImplementedError()
