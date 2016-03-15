#!/usr/bin/env python3
import random
import copy


class Schedule(object):
    @classmethod
    def from_Schedule(self, schedule):
        """
        Clone a Schedule
        """
        self._n_rooms = copy.deepcopy(schedule._n_rooms)
        self._n_times = copy.deepcopy(schedule._n_times)
        self._n_slots = copy.deepcopy(schedule._n_slots)
        self.slots = copy.deepcopy(schedule.slots)
        self.allocations = copy.copy(schedule.allocations)
        self.allocation_maps = copy.copyallocation_maps

    def __init__(self, n_times, n_rooms, allocations):
        if n_times * n_rooms < len(allocations):
            raise Exception("Too few slots")
        self._n_rooms = n_rooms
        self._n_times = n_times
        self._n_slots = n_times * n_rooms
        self.slots = [[None] * n_rooms for _ in n_times]
        self.allocations = allocations
        self.allocation_maps = dict()

    def seed_random(self):
        """
        Randomly allocates allocations to slots
        """
        choices = list(range(self._n_slots))
        random.shuffle(choices)
        for alloc, slot in zip(self.allocations, choices):
            time, room = self.slot_indices(slot)
            self.slots[time][room] = alloc
            self.allocation_maps[alloc] = (time, room)

    def slot_indices(self, slot):
        """
        Gives the indices for self.slots[][] as a tuple of (time, room)
        """
        return (slot // self._n_rooms, slot % self._n_rooms)

    def swap(self, slot1, slot2):
        """
        Swaps the allocations between two slots
        """
        time_1, room_1 = self.slot_indices(slot1)
        time_2, room_2 = self.slot_indices(slot2)
        self.slots[time_1][room_1], self.slots[time_2][room_2] = (
            self.slots[time_2][room_2], self.slots[time_1][room_1])
        for time, room in ((time_1, room_1), (time_2, room_2)):
            if self.slots[time][room] is not None:
                self.allocation_maps[self.slots[time][room]] = (time, room)

    def mutate(self, count):
        """
        Swaps randomly selected slots `count` times
        """
        for swap in range(count):
            self.swap(
                random.randrange(self._n_slots),
                random.randrange(self._n_slots))
