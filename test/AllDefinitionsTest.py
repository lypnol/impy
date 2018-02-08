#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3p
from constraint import Problem
# project
from test.Test import Test
from astree.StatementAssign import StatementAssign
from controlflow.utils import eval_path


class AllDefinitionsTest(Test):

    # for all defined variables x (defined at node label u)
    # x must be referenced in an expression later before redefined again 
    def generate_possible_paths(self, graph, u):
        statement = graph.get_statement(u)
        x = statement.var
        paths_from_u_satifiying = set()
        for path_from_u in graph.get_paths(node=u):
            redefined, referenced = False, False
            for v in path_from_u[1:-1]:
                if graph.is_def(v, x):
                    redefined = True
                    break
                if x in graph.ref(v):
                    referenced = True
                    break
            if referenced and not redefined:
                paths_from_u_satifiying.add(path_from_u)
        all_possible_paths = set()
        for path_from_u in paths_from_u_satifiying:
            for path_to_u in graph.get_paths_to(u):
                all_possible_paths.add(path_to_u[:-1]+path_from_u)
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
            or_condition = []
            possible = self.generate_possible_paths(graph, u)
            if not possible:
                continue
            for path in possible:
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
