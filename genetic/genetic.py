from common.evaluator import Evaluator

class Genetic:
    # Define parameters
    def __init__(self, evaluator: Evaluator=None):
        self.population_evaluations: list[float] # avg scores per population
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
        score = 0.0
        for chromosome in population:
            # TODO: Add parallelisation
            score += self._fitness(chromosome)
            evaluations.append(score)
        
        self.population_evaluations.append(score / len(population))
        return evaluations
    

    def _run_tournament(self, population: list[list[int]], evaluations: list[float]) -> list[list[int]]:
        raise NotImplementedError()
        """ selection = list(zip(population, evaluations))
        selection.sort(key=lambda x: x[1])
        selection = selection[len(population)/2:]
        return selection """
    

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
            # Select mate
            parents = self._run_tournament(population, evaluations)

            # Reproduce
            children = self._reproduce(parents)

            # Mutate
            children = self._mutate(children)

            # Evaluate new generation
            evaluations = self._evaluate_population(population)
            generation += 1
            
            # Test
            if self._stop_condition(generation):
                break