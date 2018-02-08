#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3p
from constraint import Problem
# project
from test.Test import Test
from controlflow.utils import eval_path


class AllILoopsTest(Test):

    def __init__(self, i):
        Test.__init__(self)
        self.i = i

    def run(self, graph, states):
        expected = set(graph.get_paths(max_whiles=self.i))
        if not expected:
            return 1
        paths = set(graph.run(state, max_whiles=self.i+1) for state in states)
        return sum([1 for path in paths if path in expected]) / len(expected)

    def generate(self, graph, timeout=10):
        test_set = set()
        paths = set(graph.get_paths(max_whiles=self.i))
        edges_paths = [[graph.get_edge(path[i], path[i+1]) for i in range(len(path)-1)] for path in paths]
        variables = sorted(graph.get_vars())
        for path in edges_paths:
            problem = Problem()
            problem.addVariables(variables, range(-100, 100))
            func = lambda *values: eval_path(path, variables, values)
            problem.addConstraint(func, variables)
            solution = problem.getSolution()
            if solution is None:
                return None
            test_set.add(frozenset(solution.items()))

        return [{k: v for k, v in state} for state in test_set]
