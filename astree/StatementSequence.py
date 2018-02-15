#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astree.Tree import Tree
from astree.ExpBoolean import ExpBoolean
from astree.StatementAssign import StatementAssign
from astree.StatementIf import StatementIf
from astree.StatementWhile import StatementWhile
from astree.StatementSkip import StatementSkip
from astree.utils import find_bloc_brackets

# Sequence statement, succession of statements
class StatementSequence(Tree):

    LABEL = 0

    @staticmethod
    def get_new_label():
        label = StatementSequence.LABEL
        StatementSequence.LABEL += 1
        return str(label)

    @staticmethod
    def parse(bloc):
        lines = bloc.split('\n')
        n = len(lines)
        sequence = []
        i = 0
        while i < n:
            line = lines[i]
            if line.startswith('#'):
                i += 1
                continue

            splitted = line.split(':')
            label = None
            if len(splitted) >= 2:
                if splitted[1][0] != "=":
                    label, line = splitted[0], ":".join(splitted[1:])
                    label = label.strip()
            line = line.strip()
            
            if not label:
                label = StatementSequence.get_new_label()

            # skip
            if not line or line == ";":
                sequence.append(StatementSkip(label=label))
                i += 1
            # assignment
            elif ':=' in line:
                sequence.append(StatementAssign.parse(line.rstrip(';'), label=label))
                i += 1
            # if
            elif line.startswith('if '):
                opening_if, closing_if = find_bloc_brackets(lines, i)
                opening_else = -1
                if closing_if < n-1 and lines[closing_if+1].strip() == 'else':
                    opening_else, closing_else = find_bloc_brackets(lines, closing_if+1)

                exp = ExpBoolean.parse(line[3:])
                statement_t = StatementSequence.parse("\n".join(lines[opening_if+1:closing_if]))
                statement_f = None
                if opening_else != -1:
                    statement_f = StatementSequence.parse("\n".join(lines[opening_else+1:closing_else]))
                sequence.append(StatementIf(exp, statement_t, statement_f, label=label))
                i = (closing_if+1) if opening_else == -1 else (closing_else+1)
            # while
            elif line.startswith('while '):
                opening, closing = find_bloc_brackets(lines, i)
                exp = ExpBoolean.parse(line[6:])
                statement = StatementSequence.parse("\n".join(lines[opening+1:closing]))
                sequence.append(StatementWhile(exp, statement, label=label))
                i = closing+1
            else:
                i += 1

        return StatementSequence(sequence)

    def __init__(self, sequence):
        Tree.__init__(self)
        self.sequence = sequence        # list of Statement obj

    def __str__(self, level=0, last=True):
        ret = Tree.__str__(self, level, last)+"\n"
        for i, statement in enumerate(self.sequence):
            ret += statement.__str__(level+1, i==len(self.sequence)-1)+("\n" if i < len(self.sequence)-1 else "")
        return ret

    def eval(self, state, catch_vars=None, include_assign=False):
        for statement in self.sequence:
            statement.eval(state, catch_vars, include_assign)
