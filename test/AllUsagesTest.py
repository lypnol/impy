#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3p
from constraint import Problem
# project
from test.Test import Test
from astree.StatementAssign import StatementAssign
from controlflow.utils import eval_path


class AllUsagesTest(Test):

    # for all defined variables x (defined at node label u)
    # x must be referenced in an expression later before redefined again 
    def generate_possible_paths(self, graph, u):
        statement = graph.get_statement(u)
        x = statement.var
        all_possible_paths_from_u = set()
        for path_from_u in graph.get_paths(node=u):
            for i, v in enumerate(path_from_u):
                if i == 0 or i == len(path_from_u)-1:
                    continue
                if graph.is_def(v, x):
                    break
                if x in graph.ref(v):
                    for path_from_v in graph.get_paths(node=v):
                        all_possible_paths_from_u.add(tuple(list(path_from_u[:i])+list(path_from_v)))
        all_possible_paths = set()
        for path_to_u in graph.get_paths_to(u):
            for path_from_u in all_possible_paths_from_u:
                path = tuple(list(path_to_u[:-1])+list(path_from_u))
                all_possible_paths.add(path)
        return all_possible_paths

    def run(self, graph, states):
        paths = set(graph.run(state) for state in states)

        assignements = graph.get_labels(StatementAssign)
        count = 0
        total = len(assignements)

        for u in assignements:
            possible = self.generate_possible_paths(graph, u)
            if not possible:
                total -= 1
            elif not possible.isdisjoint(paths):
                count += 1

        if total == 0:
            return 1

        return count / total

    def generate(self, graph, timeout=10):
        and_conditions = []
        for u in graph.get_labels(StatementAssign):
            possible = self.generate_possible_paths(graph, u)
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
