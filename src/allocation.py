#!/usr/bin/env python3


class Allocation(object):
    def __init__(self, batch, subject, teacher):
        self.batch = batch
        self.subject = subject
        self.teacher = teacher

    def __repr__(self):
        return __name__ + ".Allocation({batch}, {subject}, {teacher})".format(
            batch=repr(self.batch),
            subject=repr(self.subject),
            teacher=repr(self.teacher))
