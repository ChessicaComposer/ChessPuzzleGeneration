from common.evaluator import Evaluator
from multiprocessing import Pool
from .chromosome import Chromosome
from genetic.crossover.base import Crossover
from genetic.mutation.mutation import Mutation
from .fitness import Fitness

class Genetic:
    # Define parameters
    def __init__(self, evaluator: Evaluator = None, crossover: Crossover = None, mutation: Mutation = None,
                 fitness: Fitness = None, max_fitness: float = 10):
        self.population_evaluations: list[float] = []  # avg scores per population
        self.elevated_individuals: list[Chromosome] = []
        self.max_fitness: float = max_fitness
        self.evaluator: Evaluator = evaluator
        self.crossover: Crossover = crossover
        self.mutation: Mutation = mutation
        self.fitness: Fitness = fitness
        self.fitness.set_evaluator(evaluator)

    # Fitness function
    def _get_fitness(self, chromosome: Chromosome) -> Chromosome:
        return self.fitness.score(chromosome)

    def _mutate(self, population: list[Chromosome]) -> list[Chromosome]:
        return self.mutation.mutate(population)

    # Create population
    def _create_population(self, amount: int) -> list[Chromosome]:
        raise NotImplementedError()

    # Evaluate chromosome as thread
    def _evaluation_thread(self, chromosome: Chromosome) -> Chromosome:
        return self._get_fitness(chromosome)

    # Return list representing score of individual chromosome from population
    def _evaluate_population(self, population: list[Chromosome]) -> list[Chromosome]:
        # evaluations = [0.0 for _ in range(len(population))]
        with Pool(processes=10) as pool:
            population = pool.map(self._evaluation_thread, population)

        # Store scoring before extraction to keep track of successful generations
        scores = list(map(lambda c: c.score, population))
        joint_score = sum(scores)
        self.population_evaluations.append(joint_score / len(population))

        # Extract "perfect" individuals
        for i, chromosome in enumerate(population):
            if chromosome.score >= self.max_fitness:
                self.elevated_individuals.append(chromosome)

                # Generate replacement
                replacement = self._create_population(1)[0]
                population[i] = replacement

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
        return self.elevated_individuals
