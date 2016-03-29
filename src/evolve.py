
Population = []


def Population_seed(self, Population, meta):
    """
    Randomly seeds schedules to create a population.
    
    """
    total_population = len(Population)
    for i in range (total_population + 1):
        s = Schedule(meta['time'], meta['room'],meta['allocations'])
        s.seed_random()
        Population.append(s)
    





def Population_evolve(self, Population, Schedule, generations, fitness):
    """
    Evolves the population by repeated crossover of the fittest,
    mutation and death of the least fit schedules till a certain number of
    generations have completed or till a schedule with required fitness is obtained.

    """

    Population =  Population.sort(reverse=True, key = Schedule.fitness)
    max_fitness = Population[0].fitness
    elapsed_generations = 0
    while(max_fitness < fitness and elapsed_generations < generations):
        del Population[-1]
        del Population[-2]
        child1, child2 = crossover(Population[0], Population[1])
        Population.append(child1)     
        Population.append(child2)
        mutate(Population[-1])
        mutate(Population[-2])
        Population =  Population.sort(reverse=True, key = Schedule.fitness)
        fittest_schedule = Population[0]
        max_fitness = fittest_schedule.fitness
        elapsed_generations = elapsed_generations + 1


def Population_free(Population):
    del Population    











