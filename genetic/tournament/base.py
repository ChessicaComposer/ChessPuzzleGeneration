from genetic.chromosome import Chromosome


class Tournament:
    def run(self, population: list[Chromosome]) -> list[Chromosome]:
        raise NotImplementedError()