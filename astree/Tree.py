#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Tree:

    @staticmethod
    def parse(expression):
        raise NotImplementedError

    def __init__(self, label=None):
        self.label = label

    def __repr__(self):
        return repr(self.__str__())

    def __str__(self, level=0, last=True):
        return "    "*level+(f'({self.label}) ' if self.label else '')+self.__class__.__name__

    def eval(self, state, catch_vars=None):
        raise NotImplementedError
