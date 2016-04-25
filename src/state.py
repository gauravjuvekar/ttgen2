#!/usr/bin/env python3


class Prefs(object):
    def __init__(self):
        self.penalties = {
            'clash_time_teacher': -1000,
            'clash_time_batch': -1000,
            'room_capacity': -500}
        self._n_days = 6
        self._n_times_per_day = 8
        self.n_times = self._n_days * self._n_times_per_day
        self.mutate_counts = 3
        self.population_size = 50


class State(object):
    def __init__(self):
        self.allocations = []
        self.subjects = []
        self.teachers = []
        self.rooms = []
        self.batches = []
        self.population = []
        self.prefs = Prefs()


class RuntimeState(object):
    def __init__(self, state=None, builder=None, filename=None):
        self.builder = builder
        self.filename = filename
        self.unsaved_changes = False
        self.state = state
