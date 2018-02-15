#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astree.Tree import Tree

# If Statement
class StatementIf(Tree):
    
    def __init__(self, exp, statement_t, statement_f, label=None):
        Tree.__init__(self, label=label)
        self.exp = exp                  # ExpBool obj
        self.statement_t = statement_t  # statement to execute if expression is true SequenceStatement obj
        self.statement_f = statement_f  # statement to execute if expression is false (optional) SequenceStatement obj

    def __str__(self, level=0, last=True):
        ret = Tree.__str__(self, level, last)+"\n"
        ret += self.exp.__str__(level+1, last=False) + "\n"
        ret += self.statement_t.__str__(level+1, last=(self.statement_f is None))
        if self.statement_f:
            ret += "\n"+self.statement_f.__str__(level+1)
        return ret

    def eval(self, state, catch_vars=None, include_assign=False):
        if catch_vars is not None:
            self.exp.eval(state, catch_vars, include_assign)
            self.statement_t.eval(state, catch_vars, include_assign)
            if self.statement_f:
                self.statement_f.eval(state, catch_vars, include_assign)
            return
        if self.exp.eval(state):
            self.statement_t.eval(state)
        elif self.statement_f:
            self.statement_f.eval(state)
