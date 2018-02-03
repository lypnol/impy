#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test.Test import Test


class AllKPathsTest(Test):

    def __init__(self, k):
        Test.__init__(self)
        self.k = k

    def run(self, graph, states):
        for path in graph.get_paths(max_length=self.k):
            if not any(path == graph.run(state) for state in states):
                return False
        return True

    def generate(self, graph, to_pass, timeout=10):
        raise NotImplementedError