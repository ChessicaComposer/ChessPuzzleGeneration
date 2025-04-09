from genetic.chromosome import IntBoard

class Population:
    def get_population(self, amount: int) -> list[IntBoard]:
        raise NotImplementedError()