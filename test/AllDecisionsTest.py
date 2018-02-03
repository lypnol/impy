#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test.Test import Test
from astree.StatementIf import StatementIf
from astree.StatementWhile import StatementWhile


class AllDecisionsTest(Test):

    def run(self, graph, states):
        edges = set()
        for state in states:
            path = graph.run(state)
            edges.update(set((path[i], path[i+1]) for i in range(len(path)-1)))
        for (u, v) in graph.get_edges_from(StatementIf, StatementWhile):
            if (u, v) not in edges:
                return False
        return True

    def generate(self, graph, to_pass, timeout=10):
        raise NotImplementedError
