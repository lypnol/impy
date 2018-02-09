#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3p
from constraint import Problem
# project
from test.Test import Test
from astree.StatementAssign import StatementAssign
from controlflow.utils import eval_path


class AllUsagesTest(Test):

    def get_all_uv(self, graph):
        assignements = graph.get_labels(StatementAssign)
        for u in assignements:
            statement = graph.get_statement(u)
            x = statement.var
            for path_from_u in graph.get_paths(node=u):
                for i, v in enumerate(path_from_u):
                    if i == 0 or i == len(path_from_u)-1:
                        continue
                    if graph.is_def(v, x):
                        break
                    if x in graph.ref(v):
                        yield (u, v)

    def generate_possible_paths(self, graph, u, v):
        all_possible_paths_from_u = set()
        for path_from_u in graph.get_paths(node=u):
            i = list(path_from_u).index(v)
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
        
        count = 0
        total = 0
        for (u, v) in self.get_all_uv(graph):
            possible = self.generate_possible_paths(graph, u, v)
            if possible:
                total += 1
                if not possible.isdisjoint(paths):
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
            or_condition = []
            for path in possible:
                or_condition.append([graph.get_edge(path[i], path[i+1]) for i in range(len(path)-1)])
            and_conditions.append(or_condition)

        variables = sorted(graph.get_vars())
        test_set = set()
        for or_condition in and_conditions:
            problem = Problem()
            problem.addVariables(variables, range(-100, 100))
            func = lambda *values: any(eval_path(path, variables, values) for path in or_condition)
            problem.addConstraint(func, variables)
            solution = problem.getSolution()
            if solution is None:
                return None
            test_set.add(frozenset(solution.items()))

        return [{k: v for k, v in state} for state in test_set]
