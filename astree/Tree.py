#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Abstract tree node class
class Tree:

    # parses string expression and returns Tree node
    # :param expression: str
    @staticmethod
    def parse(expression):
        raise NotImplementedError

    def __init__(self, label=None):
        self.label = label

    def __repr__(self):
        return repr(self.__str__())

    def __str__(self, level=0, last=True):
        return "    "*level+(f'({self.label}) ' if self.label else '')+self.__class__.__name__

    # evaluate current Tree node with given variables state
    # :param state: dict variables values, would be changed after execution
    # :param catch_vars: referenced variables names list, if set to list it would be modified
    # :param include_assign: catch defined variables too
    def eval(self, state, catch_vars=None, include_assign=False):
        raise NotImplementedError
