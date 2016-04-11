import schedule

population = []


def population_seed(self, population, meta):
    """
    Randomly seeds schedules to create a population.
    """
    total_population = meta['population_count']
    population = [
        schedule.Schedule(meta['time'], meta['room'], meta['allocations']) for
        i in range(total_population)]
    for sched in population:
        sched.seed_random()


def population_evolve(self, population, Schedule, generations, fitness):
    """
    Evolves the population by repeated crossover of the fittest,
    mutation and death of the least fit schedules till a certain number of
    generations have completed or till a schedule with required fitness is
    obtained.
    """
    population = population.sort(reverse=True, key=lambda _: _.fitness())
    max_fitness = population[0].fitness()
    elapsed_generations = 0
    while(max_fitness < fitness and elapsed_generations < generations):
        del population[-1]
        del population[-2]
        child1, child2 = schedule.crossover(population[0], population[1])
        population.append(child1)
        population.append(child2)
        population[-1].mutate()
        population[-2].mutate()
        population.sort(reverse=True, key=lambda _: _.fitness())
        fittest_schedule = population[0]
        max_fitness = fittest_schedule.fitness()
        elapsed_generations += 1


def population_free(population):
    del population[:]











