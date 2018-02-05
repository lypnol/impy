#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test.Test import Test


class AllKPathsTest(Test):

    def __init__(self, k):
        Test.__init__(self)
        self.k = k

    def run(self, graph, states):
        expected = set(graph.get_paths(max_length=self.k))
        if not expected:
            return 1
        paths = set(''.join(graph.run(state)) for state in states)
        return sum([1 for path in paths if path in expected]) / len(expected)

    def generate(self, graph, timeout=10):
        raise NotImplementedError
