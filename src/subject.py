#!/usr/bin/env python3


class Subject(object):
    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return __name__ + ".Subject({name})".format(name=repr(self.name))
