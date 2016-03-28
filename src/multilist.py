#!/usr/bin/env python3


class MultiList(object):
    def __init__(self, xlen, ylen):
        self._list = [None] * xlen * ylen
        self.xlen = xlen
        self.ylen = ylen

    def int_index(self, index):
        if isinstance(index, tuple):
            return index[0] * self.xlen + index[1]
        elif isinstance(index, int):
            return index
        else:
            raise TypeError("`index` must be tuple or int")

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = self.int_index(index.start) if index is not None else None
            end = self.int_index(index.end) if index is not None else None
            return self._list[start:end:index.step]
        else:
            return self._list[self.int_index(index)]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            start = self.int_index(index.start) if index is not None else None
            end = self.int_index(index.end) if index is not None else None
            self._list[start:end:index.step] = value
        else:
            self._list[self.int_index(index)] = value