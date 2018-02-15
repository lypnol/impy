#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# checks if given variables state goses through given path
# :param path: list of ControlFlowGraph edges [[ExpBool, Statement]]
# :param variables: list of variable names str
# :param values: list of corresponding variables values int
def eval_path(path, variables, values):
    state = {variables[i]: values[i] for i in range(len(variables))}
    for exp, statement in path:
        if exp.eval(state):
            statement.eval(state)
        else:
            return False
    return True
