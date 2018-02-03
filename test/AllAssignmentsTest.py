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
        paths = set()
        for state in states:
            paths.update(set(graph.run(state)))
        for label in graph.get_labels(StatementAssign):
            if label not in paths:
                return False
        return True

    def generate(self, graph, to_pass, timeout=10):
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
            problem.addVariables(variables, [i for i in range(-1000, 1000)])
            if to_pass:
                func = lambda *values: any(eval_path(path, variables, values) for path in condition)
            else:
                func = lambda *values: all(not eval_path(path, variables, values) for path in condition)
            problem.addConstraint(func, variables)
            solution = problem.getSolution()
            if to_pass:
                if solution is None:
                    return None
                test_set.add(frozenset(solution.items()))
            elif solution is not None:
                return [solution]

        return [{k: v for k, v in state} for state in test_set]
