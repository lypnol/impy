#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test.Test import Test


class AllILoopsTest(Test):

    def __init__(self, i):
        Test.__init__(self)
        self.i = i

    def run(self, graph, states):
        paths = set(''.join(graph.run(state)) for state in states)
        for path in graph.get_paths(max_whiles=self.i):
            if path not in paths:
                return False
        return True

    def generate(self, graph, to_pass, timeout=10):
        raise NotImplementedError
