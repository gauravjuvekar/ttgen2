#!/usr/bin/env python3


class Prefs(object):
    def __init__(self):
        self.penalties = {
            'clash_time_teacher': -1000,
            'clash_time_batch': -1000}
        self.n_times = None
        self.mutate_counts = None
        self.population_size = None


class Meta(object):
    def __init__(self):
        self.allocations = []
        self.subjects = []
        self.teachers = []
        self.rooms = []
        self.batches = []
        self.population = []
        self.prefs = Prefs()
