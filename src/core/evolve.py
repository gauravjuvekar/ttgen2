import logging
logger = logging.getLogger(__name__)

from core import schedule


def population_seed(state):
    """
    Randomly seeds schedules to create a population.
    """
    total_population = state.prefs.population_size
    del state.population[total_population:]
    extend_by = total_population - len(state.population)
    state.population.extend([
        schedule.Schedule(
            state.prefs.n_times,
            len(state.rooms),
            state.allocations) for
        _ in range(extend_by)])
    for sched in state.population:
        sched.seed_random()


def population_evolve(state, generations, fitness):
    """
    Evolves the population by repeated crossover of the fittest,
    mutation and death of the least fit schedules till a certain number of
    generations have completed or till a schedule with required fitness is
    obtained.
    """
    population_seed(state)
    state.population.sort(reverse=True, key=lambda _: _.fitness)
    max_fitness = state.population[0].fitness
    elapsed_generations = 0
    while(max_fitness < fitness and elapsed_generations < generations):
        del state.population[-1]
        del state.population[-2]
        child1 = schedule.Schedule.from_Schedule(state.population[0])
        child2 = schedule.Schedule.from_Schedule(state.population[1])
        child1, child2 = schedule.crossover(child1, child2)
        state.population.append(child1)
        state.population.append(child2)
        state.population[-1].mutate2(state.prefs.mutate_counts)
        state.population[-2].mutate2(state.prefs.mutate_counts)
        state.population.sort(reverse=True, key=lambda _: _.fitness)
        fittest_schedule = state.population[0]
        max_fitness = fittest_schedule.fitness
        elapsed_generations += 1
