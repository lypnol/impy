#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def eval_path(path, variables, values):
    state = {variables[i]: values[i] for i in range(len(variables))}
    for exp, statement in path:
        if exp.eval(state):
            statement.eval(state)
        else:
            return False
    return True
