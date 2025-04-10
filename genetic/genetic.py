from common.evaluator import Evaluator
from multiprocessing import Pool
from .chromosome import Chromosome
from genetic.crossover.base import Crossover
from genetic.mutation.base import Mutation
from .fitness.base import Fitness
from .population.base import Population
from .tournament.base import Tournament

from .crossover import Crossover
from .mutation import Mutation
from .fitness import Fitness
from common.conditions import Conditions
import time

class Genetic:
    # Define parameters
    def __init__(self,
                 evaluator: Evaluator = None,
                 crossover: Crossover = None,
                 mutation: Mutation = None,
                 fitness: Fitness = None,
                 population: Population = None,
                 tournament: Tournament = None,
                 max_fitness: float = 10):
        self.population_evaluations: list[float] = []  # avg scores per population
        self.elevated_individuals: list[Chromosome] = []
        self.max_fitness: float = max_fitness
        self.evaluator: Evaluator = evaluator
        self.crossover: Crossover = crossover
        self.mutation: Mutation = mutation
        self.fitness: Fitness = fitness
        self.population: Population = population
        self.tournament: Tournament = tournament
        self.fitness.set_evaluator(evaluator)

    # Evaluate chromosome as thread
    def _evaluation_thread(self, chromosome: Chromosome) -> Chromosome:
        return self.fitness.score(chromosome)

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
                replacement = self.population.create(1)[0]
                population[i] = replacement

        return population

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
        population = self.population.create(population_size)

        # Initial evaluation
        population = self._evaluate_population(population)

        generation = 0
        stop_condition = False
        # Evaluate cost
        while(not stop_condition):
            print("Generation " + str(generation + 1))
            # Select mate
            parents = self.tournament.run(population)

            # Reproduce
            children = self.crossover.reproduce(parents)

            # Mutate
            children = self.mutation.mutate(children)

            # Update population
            population = parents + children

            # Evaluate new generation
            population = self._evaluate_population(population)
            generation += 1

            # Check if conditions have been met
            current_conditions = Conditions(time.time() - start, generation,max(list(map(lambda c: c.score, population))))
            stop_condition = self._stop_condition(current_conditions, conditions)

        print(self.population_evaluations)
        return self.elevated_individuals
