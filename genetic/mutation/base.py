from genetic.chromosome import Chromosome

class Mutation:
    def __init__(self):
        pass

    def mutate(self, population: list[Chromosome]) -> list[Chromosome]:
        raise NotImplementedError()
