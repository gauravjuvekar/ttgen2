#!/usr/bin/env python3


class Batch(object):
    def __init__(self, name, n_students):
        self.name = name
        self.n_students = n_students

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return __name__ + ".Batch({name}, {n_students})".format(
            name=repr(self.name),
            n_students=repr(self.n_students))
