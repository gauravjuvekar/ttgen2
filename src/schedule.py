#!/usr/bin/env python3
import random
import copy
from collections import namedtuple


class Schedule(object):
    SlotIndex = namedtuple('SlotIndex', ['time', 'room'])

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
            slot = self.slot_indices(slot)
            self.slots[slot.time][slot.room] = alloc
            self.allocation_maps[alloc] = slot

    def slot_indices(self, slot):
        """
        Gives the indices for self.slots[][] as a tuple of (time, room)
        """
        return self.SlotIndex(
            time=(slot // self._n_rooms),
            room=(slot % self._n_rooms))

    def swap(self, slot1, slot2):
        """
        Swaps the allocations between two slots
        """
        slot1 = self.slot_indices(slot1)
        slot2 = self.slot_indices(slot2)
        self.slots[slot1.time][slot1.room],
        self.slots[slot2.time][slot2.room] = (
            self.slots[slot2.time][slot2.room],
            self.slots[slot1.time][slot1.room])
        for slot in (slot1, slot2):
            if self.slots[slot.time][slot.room] is not None:
                self.allocation_maps[self.slots[slot.time][slot.room]] = slot

    def mutate(self, count):
        """
        Swaps randomly selected slots `count` times
        """
        for swap in range(count):
            self.swap(
                random.randrange(self._n_slots),
                random.randrange(self._n_slots))

    def fitness(self):
        penalties = dict()
        penalties['clash_time_teacher'] = -1000
        penalties['clash_time_batch'] = -1000

        fitness = 0

        # teacher time clashes
        for time_slot in self.slots:
            teachers = dict()
            for allocation in time_slot:
                try:
                    teachers[allocation.teacher] += 1
                except KeyError:
                    teachers[allocation.teacher] = 1
            violations = sum((
                (count - 1) for count in teachers.values() if count > 1))
            fitness += violations * penalties['clash_time_teacher']

        # batches time clashes
        for time_slot in self.slots:
            batches = dict()
            for allocation in time_slot:
                try:
                    batches[allocation.batch] += 1
                except KeyError:
                    batches[allocation.batch] = 1
            violations = sum((
                (count - 1) for count in batches.values() if count > 1))
            fitness += violations * penalties['clash_time_batch']

        return fitness

    def mutate2(self, count):
        """ Selected two points always different """
        for swap in range(count):
            swap1 = random.randrange(self._n_slots)
            swap2 = random.randrange(self._n_slots)
            while(swap2 == swap1):
                swap2 = random.randrange(self._n_slots)
            self.swap(swap1, swap2)

    def shuffle_swap(self, slot1, slot2):
        slot1 = self.slot_indices(slot1)
        slot2 = self.slot_indices(slot2)

        """ Need to shuffle all the slots between the two points"""
        shuffled_part = self.slots[
            slot1.time:slot2.time][slot1.room:slot2.room]
        random.shuffle(shuffled_part)
        self.slots[slot1.time:slot2.time][slot1.room:slot2.room] = (
            shuffled_part)

        for slot in (slot1, slot2):
            if self.slots[slot.time][slot.room] is not None:
                self.allocation_maps[self.slots[slot.time][slot.room]] = slot

    def mutate3(self, count):
        """ Shuffling randomly between two points """
        for swap in range(count):
            swap1 = random.randrange(self._n_slots)
            swap2 = random.randrange(self._n_slots)
            while(swap2 == swap1):
                swap2 = random.randrange(self._n_slots)
        self.shuffle_swap(self, swap1, swap2)
