from common.evaluator import Evaluator


class Genetic:
    # Define parameters
    def __init__(self, evaluator: Evaluator = None):
        self.population_evaluations: list[float] = []  # avg scores per population
        self.evaluator: Evaluator = evaluator

    # Fitness function
    def _fitness(self, chromosome: list[int]) -> float:
        raise NotImplementedError()

    def _mutate(self, population: list[list[int]]) -> list[list[int]]:
        raise NotImplementedError()

    # Create population
    def _create_population(self, amount: int) -> list[list[int]]:
        raise NotImplementedError()

    # Return list representing score of individual chromosome from population
    def _evaluate_population(self, population: list[list[int]]) -> list[float]:
        evaluations = []
        joint_score = 0.0
        for chromosome in population:
            # TODO: Add parallelisation
            score = self._fitness(chromosome)
            joint_score += score
            evaluations.append(score)

        self.population_evaluations.append(joint_score / len(population))
        return evaluations

    def _run_tournament(self, population: list[list[int]], evaluations: list[float]) -> list[list[int]]:
        raise NotImplementedError()

    def _reproduce(self, population: list[list[int]]) -> list[list[int]]:
        raise NotImplementedError()

    def _stop_condition(self, generation) -> bool:
        raise NotImplementedError()

    def run(self, generations: int, population_size: int):
        # Initialize population
        population = self._create_population(population_size)

        # Initial evaluation
        evaluations = self._evaluate_population(population)

        generation = 0

        # Evaluate cost
        for _ in range(generations):
            print("Generation " + str(generation + 1))
            # Select mate
            parents = self._run_tournament(population, evaluations)

            # Reproduce
            children = self._reproduce(parents)

            # Mutate
            children = self._mutate(children)

            # Update population
            population = parents + children

            # Evaluate new generation
            evaluations = self._evaluate_population(population)
            print(evaluations)
            generation += 1

            # Test
            if self._stop_condition(generation):
                break

        print(self.population_evaluations)
        return population, evaluations