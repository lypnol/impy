#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astree.Tree import Tree

# Skip statement
class StatementSkip(Tree):

    def __init__(self, label=None):
        Tree.__init__(self, label=label)

    def eval(self, state, catch_vars=None, include_assign=False):
        pass

    def to_exp(self):
        return "skip"