#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3p
from constraint import Problem
# project
from test.Test import Test
from astree.StatementIf import StatementIf
from astree.StatementWhile import StatementWhile
from controlflow.utils import eval_path


class AllConditionsTest(Test):

    def run(self, graph, states):
        total = 0
        count = 0

        for u in graph.get_labels(StatementIf, StatementWhile):
            statement = graph.get_statement(u)
            conditions = []
            for condition in statement.exp.get_conditions():
                variables = []
                condition.eval({}, catch_vars=variables)
                if set(variables):
                    conditions.append(condition)
            total += len(conditions)
            found = all((
                any(condition.eval(state) for state in states) and 
                any(not condition.eval(state) for state in states)
            ) for condition in conditions)
            if found:
                count += 1
        return count / total

    def generate(self, graph, timeout=10):
        all_variables = sorted(graph.get_vars(include_assign=True))
        test_set = set()
        for u in graph.get_labels(StatementIf, StatementWhile):
            statement = graph.get_statement(u)
            conditions = statement.exp.get_conditions()
            for condition in conditions:
                variables = []
                condition.eval({}, catch_vars=variables)
                variables = sorted(set(variables))
                if not variables:
                    continue
                for val in [True, False]:
                    problem = Problem()
                    problem.addVariables(variables, range(-100, 100))
                    if val:
                        func = lambda *values: condition.eval({k: values[i] for i, k in enumerate(variables)})
                    else:
                        func = lambda *values: not condition.eval({k: values[i] for i, k in enumerate(variables)})
                    problem.addConstraint(func, variables)
                    solution = problem.getSolution()
                    if solution is None:
                        return None
                    for variable in all_variables:
                        if variable not in solution:
                            solution[variable] = 0
                    test_set.add(frozenset(solution.items()))
        return [{k: v for k, v in state} for state in test_set]
