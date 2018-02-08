#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astree.Tree import Tree
from astree.ExpArithmetic import ExpArithmetic


class StatementAssign(Tree):

    @staticmethod
    def parse(expression, label=None):
        # remove all whitespace characters
        expression = ''.join(expression.split())
        var, exp = expression.split(':=')
        return StatementAssign(var, ExpArithmetic.parse(exp), label=label)

    def __init__(self, var, arithmetic_exp, label=None):
        Tree.__init__(self, label=label)
        self.var = var
        self.arithmetic_exp = arithmetic_exp

    def __str__(self, level=0, last=True):
        ret = Tree.__str__(self, level, last)+f" [{self.var}]"+"\n"
        ret += self.arithmetic_exp.__str__(level+1)
        return ret

    def eval(self, state, catch_vars=None, include_assign=False):
        if (catch_vars is not None and include_assign):
            catch_vars.append(self.var)
        state[self.var] = self.arithmetic_exp.eval(state, catch_vars)

    def to_exp(self):
        return f'{self.var} := {self.arithmetic_exp.to_exp()}'
