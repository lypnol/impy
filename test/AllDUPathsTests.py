#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3p
from constraint import Problem
# project
from test.AllUsagesTest import AllUsagesTest
from controlflow.utils import eval_path


class AllDUPathsTests(AllUsagesTest):

    def run(self, graph, states):
        paths = set(graph.run(state) for state in states)
        
        count = 0
        total = 0
        for (u, v) in self.get_all_uv(graph):
            possible = self.generate_possible_paths(graph, u, v)
            if possible:
                total += 1
                if possible.issubset(paths):
                    count += 1

        if total == 0:
            return 1

        return count / total

    def generate(self, graph, timeout=10):
        and_conditions = []
        for (u, v) in self.get_all_uv(graph):
            possible = self.generate_possible_paths(graph, u, v)
            if not possible:
                continue
            for path in possible:
                and_conditions.append([graph.get_edge(path[i], path[i+1]) for i in range(len(path)-1)])

        variables = sorted(graph.get_vars())
        test_set = set()
        for path in and_conditions:
            problem = Problem()
            problem.addVariables(variables, range(-100, 100))
            func = lambda *values: eval_path(path, variables, values)
            problem.addConstraint(func, variables)
            solution = problem.getSolution()
            if solution is None:
                return None
            test_set.add(frozenset(solution.items()))

        return [{k: v for k, v in state} for state in test_set]
