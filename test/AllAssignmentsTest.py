#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3p
from constraint import Problem
# project
from test.Test import Test
from astree.StatementAssign import StatementAssign
from controlflow.utils import eval_path


class AllAssignmentsTest(Test):

    def run(self, graph, states):
        expected = set(graph.get_labels(StatementAssign))
        if not expected:
            return 1
        labels = set()
        for state in states:
            labels.update(set(graph.run(state)))
        return sum([1 for label in labels if label in expected]) / len(expected)

    def generate(self, graph, timeout=10):
        and_conditions = []
        for u in graph.get_labels(StatementAssign):
            or_condition = []
            for path in graph.get_paths_to(u):
                or_condition.append([graph.get_edge(path[i], path[i+1]) for i in range(len(path)-1)])
            and_conditions.append(or_condition)
            
        variables = sorted(graph.get_vars())
        test_set = set()
        for condition in and_conditions:
            problem = Problem()
            problem.addVariables(variables, range(-100, 100))
            func = lambda *values: any(eval_path(path, variables, values) for path in condition)
            problem.addConstraint(func, variables)
            solution = problem.getSolution()
            if solution is None:
                return None
            test_set.add(frozenset(solution.items()))

        return [{k: v for k, v in state} for state in test_set]
