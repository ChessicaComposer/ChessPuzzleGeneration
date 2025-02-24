class Genetic:
    # Define parameters
    def __init__(self):
        self.population_evaluations: list[float] # avg scores per population


    # Fitness function
    def __fitness(self) -> float:
        raise NotImplementedError()
    

    def __mutate(self, population: list[list[int]]) -> list[list[int]]:
        raise NotImplementedError()


    # Create population
    def __create_population(self) -> list[list[int]]:
        raise NotImplementedError()
    

    # Return list representing score of individual chromosome from population
    def __evaluate_population(self, population: list[list[int]]) -> list[float]:
        evaluations = []
        score = 0.0
        for chromosome in population:
            # TODO: Add parallelisation
            score += self.__fitness(chromosome)
            evaluations.append(score)
        
        self.population_evaluations.append(score / len(population))
        return evaluations
    

    def __run_tournament(self, population: list[list[int]], evaluations: list[float]) -> list[list[int]]:
        raise NotImplementedError()
        """ selection = list(zip(population, evaluations))
        selection.sort(key=lambda x: x[1])
        selection = selection[len(population)/2:]
        return selection """
    

    def __reproduce(self, population: list[list[int]]) -> list[list[int]]:
        raise NotImplementedError()
    
    
    def __stop_condition(self, generation) -> bool:
        raise NotImplementedError()


    def run(self, generations):
        # Initialize population
        population = self.__create_population()
        
        # Initial evaluation
        evaluations = self.__evaluate_population(population)

        generation = 0
        
        # Evaluate cost
        for _ in range(generations):
            # Select mate
            parents = self.__run_tournament(population, evaluations)

            # Reproduce
            children = self.__reproduce(parents)

            # Mutate
            children = self.__mutate(children)

            # Evaluate new generation
            evaluations = self.__evaluate_population(population)
            generation += 1
            
            # Test
            if self.__stop_condition(generation):
                break