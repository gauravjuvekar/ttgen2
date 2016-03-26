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


    def swap_chunk(self, slot1, slot2, Schedule_1, Schedule_2):
        """
        Swap the chunk of allocations between the two 
        indices crossover1(slot1) & crossover2(slot2)
        of two parent allocations.

        The parents are cloned to form the children.

        """

        child1 = from_Schedule(Schedule_1)
        child2 = from_Schedule(Schedule_2)

        p1_time_1, p1_room_1 = Schedule_1.slot_indices(slot1)
        p1_time_2, p1_room_2 = Schedule_1.slot_indices(slot2)    

        p2_time_1, p2_room_1 = Schedule_2.slot_indices(slot1)
        p2_time_2, p2_room_2 = Schedule_2.slot_indices(slot2)


        for time, room in range((p2_time_1, p2_room_1), ((p2_time_2 + 1), (p2_room_2 + 1))):
            if Schedule_2.slots[time][room] is not None:
                child1.allocation_maps[Schedule_2.slots[time][room]] = (time, room)

        for time, room in range((p1_time_1, p1_room_1), ((p1_time_2 + 1), (p1_room_2 + 1))):
            if Schedule_1.slots[time][room] is not None:
                child2.allocation_maps[Schedule_1.slots[time][room]] = (time, room)


        return child1, child2


    def crossover(self, Schedule_1, Schedule_2, count):
        """
        Combine two parent allocations into two offsprings
        by swapping randomly determined chunk.

        """

        crossover1 = random.randrange(self._n_slots)
        crossover2 = random.randrange(crossover1 + 1, self._n_slots + 1)

    
        for swap_chunk in range(count):
            swap_chunk(crossover1, crossover2, Schedule_1, Schedule_2)        






