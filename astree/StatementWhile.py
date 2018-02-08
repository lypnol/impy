#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astree.Tree import Tree


class StatementWhile(Tree):

    def __init__(self, exp, statement, label=None):
        Tree.__init__(self, label=label)
        self.exp = exp
        self.statement = statement

    def __str__(self, level=0, last=True):
        ret = Tree.__str__(self, level, last)+"\n"
        ret += self.exp.__str__(level+1, last=False) + "\n"
        ret += self.statement.__str__(level+1)
        return ret

    def eval(self, state, catch_vars=None, include_assign=False):
        if catch_vars is not None:
            self.exp.eval(state, catch_vars, include_assign)
            self.statement.eval(state, catch_vars, include_assign)
            return
        while self.exp.eval(state):
            self.statement.eval(state)
