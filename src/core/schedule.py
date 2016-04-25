#!/usr/bin/env python3
import random
from collections import namedtuple

import logging
logger = logging.getLogger(__name__)

from core import multilist


class Schedule(object):
    SlotIndex = namedtuple('SlotIndex', ['time', 'room'])

    @classmethod
    def from_Schedule(cls, schedule):
        """
        Clone a Schedule
        """
        self = cls.__new__(cls)
        self._n_rooms = schedule._n_rooms
        self._n_times = schedule._n_times
        self._n_slots = schedule._n_slots
        self.slots = multilist.MultiList(
            schedule._n_rooms,
            schedule._n_times,
            schedule.slots[:])
        assert self.slots._list == schedule.slots._list
        self.state = schedule.state
        self.allocation_maps = schedule.allocation_maps.copy()
        self._fitness = schedule._fitness
        self._fitness_valid = schedule._fitness_valid
        return self

    def __init__(self, n_times, n_rooms, state):
        if n_times * n_rooms < len(state.allocations):
            raise Exception("Too few slots")
        self._n_rooms = n_rooms
        self._n_times = n_times
        self._n_slots = n_times * n_rooms
        self.slots = multilist.MultiList(n_rooms, n_times)
        self.state = state
        self.allocation_maps = dict()
        self._fitness = None
        self._fitness_valid = False

    @property
    def fitness(self,):
        if not self._fitness_valid:
            fitness = 0
            # teacher time clashes
            room_capacity_overflow = 0
            for time_slot in self.slots[(None, None): (None, None)]:
                teachers = dict()
                batches = dict()
                for room, allocation in enumerate(time_slot):
                    if allocation is not None:
                        try:
                            teachers[allocation.teacher] += 1
                        except KeyError:
                            teachers[allocation.teacher] = 1
                        try:
                            batches[allocation.batch] += 1
                        except KeyError:
                            batches[allocation.batch] = 1
                        diff_capacity = (
                            allocation.batch.n_students -
                            self.state.rooms[room].capacity)
                        if diff_capacity > 0:
                            room_capacity_overflow += diff_capacity
                teacher_clashes = sum((
                    (count - 1) for count in teachers.values() if count > 1))
                fitness += (
                    teacher_clashes *
                    self.state.prefs.penalties['clash_time_teacher'])
                batch_clashes = sum((
                    (count - 1) for count in batches.values() if count > 1))
                fitness += (
                    batch_clashes *
                    self.state.prefs.penalties['clash_time_batch'])
            fitness += (
                room_capacity_overflow *
                self.state.prefs.penalties['room_capacity'])
            self._fitness = fitness
            self._fitness_valid = True
            logger.debug("Fitness recalculated to %s", self._fitness)
        else:
            logger.debug("Fitness already cached (%s)", self._fitness)
        return self._fitness

    @fitness.setter
    def fitness(self):
        raise AttributeError("'fitness' is read only")

    def seed_random(self):
        """
        Randomly allocates allocations to slots
        """
        choices = list(range(self._n_slots))
        random.shuffle(choices)
        for alloc, slot in zip(self.state.allocations, choices):
            self.slots[slot] = alloc
            self.allocation_maps[alloc] = slot
        self._fitness_valid = False

    def slot_indices(self, slot):
        """
        Gives the indices for self.slots[][] as a tuple of (time, room)
        """
        return self.SlotIndex(
            time=(slot // self._n_rooms),
            room=(slot % self._n_rooms))

    def slot_int(self, slot):
        """
        Gives the integer index for a tuple of (time, room)
        """
        if isinstance(slot, tuple):
            return slot[0] * self._n_rooms + slot[1]
        else:
            return slot

    def swap(self, slot1, slot2):
        """
        Swaps the allocations between two slots
        """
        self.slots[slot1], self.slots[slot2] = (
            self.slots[slot2],
            self.slots[slot1])
        for slot in (slot1, slot2):
            if self.slots[slot] is not None:
                self.allocation_maps[self.slots[slot]] = self.slot_int(slot)
        self._fitness_valid = False

    def mutate(self, count):
        """ Selected two points always different """
        for swap in range(count):
            swap1 = random.randrange(self._n_slots)
            swap2 = random.randrange(self._n_slots)
            while(swap2 == swap1):
                swap2 = random.randrange(self._n_slots)
            self.swap(swap1, swap2)
        self._fitness_valid = False

    def closest_vacant(self, slot):
        """
        Returns the closest vacant slot to `slot` (or `slot` itself if it is
        vacant)
        """
        def seq_gen(slot, max_len, min_len=0):
            yield slot
            lo = hi = slot
            lo -= 1
            hi += 1
            while lo >= 0 or hi < max_len:
                if lo >= 0:
                    yield lo
                    lo -= 1
                if hi < max_len:
                    yield hi
                    hi += 1
            else:
                raise StopIteration()
        for slot in seq_gen(slot, max_len=len(self.slots)):
            if self.slots[slot] is None:
                return slot
        else:
            raise RuntimeError("No vacant slot")


def swap_allocations(point_1, point_2, schedule1, schedule2):
    """
    Swap the chunk of allocations between point_1 and point_2

    The parents are cloned to form the children.
    """
    for alloc in range(point_1, point_2):
        alloc = schedule1.state.allocations[alloc]
        schedule1.slots[schedule1.allocation_maps[alloc]] = None
        schedule2.slots[schedule2.allocation_maps[alloc]] = None
    for alloc in range(point_1, point_2):
        alloc = schedule1.state.allocations[alloc]
        schedule1.allocation_maps[alloc], schedule2.allocation_maps[alloc] = (
            schedule1.closest_vacant(schedule2.allocation_maps[alloc]),
            schedule2.closest_vacant(schedule1.allocation_maps[alloc]))
        schedule1.slots[schedule1.allocation_maps[alloc]] = alloc
        schedule2.slots[schedule2.allocation_maps[alloc]] = alloc
    schedule1._fitness_valid = False
    schedule2._fitness_valid = False


def crossover_two_point(schedule1, schedule2):
    """
    The schedules will be modified
    Clone them separately first
    """
    point_1 = random.randrange(len(schedule1.state.allocations))
    point_2 = random.randrange(point_1, len(schedule1.state.allocations))
    swap_allocations(point_1, point_2, schedule1, schedule2)
