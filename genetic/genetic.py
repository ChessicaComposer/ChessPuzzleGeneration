from common.evaluator import Evaluator
from multiprocessing import Pool
from .chromosome import Chromosome
from .crossover import Crossover
from .mutation import Mutation
from .fitness import Fitness
from common.conditions import Conditions
import time

class Genetic:
    # Define parameters
    def __init__(self, evaluator: Evaluator = None, crossover: Crossover = None, mutation: Mutation = None, fitness: Fitness = None):
        self.population_evaluations: list[float] = []  # avg scores per population
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
        scores = list(map(lambda c: c.score, population))
        joint_score = sum(scores)
        self.population_evaluations.append(joint_score / len(population))
        return population

    def _run_tournament(self, population: list[Chromosome]) -> list[Chromosome]:
        raise NotImplementedError()

    def _reproduce(self, population: list[Chromosome]) -> list[Chromosome]:
        return self.crossover.reproduce(population)

    def _stop_condition(self, current: Conditions, conditions: Conditions) -> bool:
        if current.time_limit >= conditions.time_limit:
            return True
        if current.generation_limit >= conditions.generation_limit:
            return True
        if current.evaluation_limit >= conditions.evaluation_limit:
            return True
        return False
    
    def run(self, conditions: Conditions, population_size: int):
        
        # Start time
        start = time.time()
        
        # Initialize population
        population = self._create_population(population_size)

        # Initial evaluation
        population = self._evaluate_population(population)

        generation = 0
        stop_condition = False
        # Evaluate cost
        while(not stop_condition):
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

            # Check if conditions have been met
            current_conditions = Conditions(time.time() - start, generation,max(list(map(lambda c: c.score, population))))
            stop_condition = self._stop_condition(current_conditions, conditions)

        print(self.population_evaluations)
        return population
