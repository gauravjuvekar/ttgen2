import logging
logger = logging.getLogger(__name__)

from core import schedule


def population_seed(state):
    """
    Randomly seeds schedules to create a population.
    """
    total_population = state.prefs.population_size
    logger.debug("Seeding to attain %s", total_population)
    del state.population[total_population:]
    extend_by = total_population - len(state.population)
    logger.debug("Extending population by %s", extend_by)
    extension = [
        schedule.Schedule(
            state.prefs.n_times,
            len(state.rooms),
            state) for
        _ in range(extend_by)]
    logger.debug("Reseeding newer schedules")
    for sched in extension:
        sched.seed_random()
    state.population.extend(extension)


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
        logger.debug("Cloned parents")
        logger.debug(
            "count(None) in child1 %s", child1.slots._list.count(None))
        logger.debug(
            "count(None) in child2 %s", child2.slots._list.count(None))
        schedule.crossover_two_point(child1, child2)
        logger.debug("Crossed over")
        logger.debug(
            "count(None) in child1 %s", child1.slots._list.count(None))
        logger.debug(
            "count(None) in child2 %s", child2.slots._list.count(None))
        state.population.append(child1)
        state.population.append(child2)
        state.population[-1].mutate(state.prefs.mutate_counts)
        state.population[-2].mutate(state.prefs.mutate_counts)
        logger.debug("Mutated")
        logger.debug(
            "count(None) in child1 %s", child1.slots._list.count(None))
        logger.debug(
            "count(None) in child2 %s", child2.slots._list.count(None))
        state.population.sort(reverse=True, key=lambda _: _.fitness)
        fittest_schedule = state.population[0]
        max_fitness = fittest_schedule.fitness
        elapsed_generations += 1
