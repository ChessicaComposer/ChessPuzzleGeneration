from genetic.chromosome import IntBoard


class Tournament:
    def __init__(self, population: list[IntBoard]):
        self.population = population

    def run_tournament(self, population: list[IntBoard]) -> list[IntBoard]:
        raise NotImplementedError()