from genetic.chromosome import IntBoard

class Population:
    def create(self, amount: int) -> list[IntBoard]:
        raise NotImplementedError()