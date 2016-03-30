#!/usr/bin/env python3


class Room(object):
    def __init__(self, name, capacity, pk=None):
        self.pk = pk
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return __name__ + ".Room({name}, {capacity}, {pk})".format(
            name=repr(self.name),
            capacity=repr(self.capacity),
            pk=repr(self.pk))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
