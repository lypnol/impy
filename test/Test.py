#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Abstract coverage test class
class Test:

    # Runs a coverage test on given graph 
    # against given entry states
    def run(self, graph, states):
        raise NotImplementedError

    # Generate an entry state set to pass coverage test
    def generate(self, graph, timeout=10):
        raise NotImplementedError

    def __repr__(self):
        return repr(str(self))

    def __str__(self):
        return self.__class__.__name__
