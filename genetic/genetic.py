from common.evaluator import Evaluator
from multiprocessing import Pool
from .chromosome import Chromosome
from .crossover import Crossover
from .mutation import Mutation

class Genetic:
    # Define parameters
    def __init__(self, evaluator: Evaluator = None, crossover: Crossover = None, mutation: Mutation = None):
        self.population_evaluations: list[float] = []  # avg scores per population
        self.evaluator: Evaluator = evaluator
        self.crossover: Crossover = crossover
        self.mutation: Mutation = mutation

    # Fitness function
    def _fitness(self, chromosome: Chromosome) -> Chromosome:
        raise NotImplementedError()

    def _mutate(self, population: list[Chromosome]) -> list[Chromosome]:
        return self.mutation.mutate(population)

    # Create population
    def _create_population(self, amount: int) -> list[Chromosome]:
        raise NotImplementedError()

    # Evaluate chromosome as thread
    def _evaluation_thread(self, chromosome: Chromosome) -> Chromosome:
        return self._fitness(chromosome)

    # Return list representing score of individual chromosome from population
    def _evaluate_population(self, population: list[Chromosome]) -> list[Chromosome]:
        # evaluations = [0.0 for _ in range(len(population))]
        with Pool(processes=10) as pool:
            population = pool.map(self._evaluation_thread, population)
        scores = list(map(lambda c: c.score, population))
        joint_score = sum(scores)
        self.population_evaluations.append(joint_score / len(population))
        return population

    def _run_tournament(self, population: list[Chromosome]) -> list[Chromosome]:
        raise NotImplementedError()

    def _reproduce(self, population: list[Chromosome]) -> list[Chromosome]:
        return self.crossover.reproduce(population)

    def _stop_condition(self, generation) -> bool:
        raise NotImplementedError()

    def run(self, generations: int, population_size: int):
        # Initialize population
        population = self._create_population(population_size)

        # Initial evaluation
        population = self._evaluate_population(population)

        generation = 0

        # Evaluate cost
        for _ in range(generations):
            print("Generation " + str(generation + 1))
            # Select mate
            parents = self._run_tournament(population)

            # Reproduce
            children = self._reproduce(parents)

            # Mutate
            children = self._mutate(children)

            # Update population
            population = parents + children

            # Evaluate new generation
            population = self._evaluate_population(population)
            generation += 1

            # Test
            if self._stop_condition(generation):
                break

        print(self.population_evaluations)
        return population
