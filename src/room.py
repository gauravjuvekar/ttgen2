#!/usr/bin/env python3


class Room(object):
    def __init__(self, name, capacity, pk=None):
        self.pk = pk
        self.name = name
        self.capacity = capacity
