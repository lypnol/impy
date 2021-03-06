#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astree.Tree import Tree
from astree.ExpArithmetic import ExpArithmetic
from astree.utils import find_bloc_brackets


BINOP_BOOL = ['||', '&&']
BINOP_ARIT = ['<', '>', '<=', '>=', '==', '!=']
BINOP = BINOP_BOOL + BINOP_ARIT
BINOP_START = [op[0] for op in BINOP]

UNAOP = ['!']

class InvalidBooleanExpression(Exception): pass

# Boolean expression tree node
class ExpBoolean(Tree):

    @staticmethod
    def parse(expression):
        if expression == '':
            return None
        # remove all whitespace characters
        expression = ''.join(expression.split())

        if expression[0] == '(':
            opening, closing = find_bloc_brackets(expression, bracket='(')
            if closing == -1:
                raise InvalidBooleanExpression(f'Invalid boolean expression {expression}')
            if closing == len(expression) - 1:
                return ExpBoolean.parse(expression[opening+1:closing])
            op = expression[closing+1]
            if op in ['<', '>']:
                if closing < len(expression)-2 and expression[closing+2] == '=':
                    op += expression[closing+2]
            else:
                op += expression[closing+2]

            if op not in BINOP:
                raise InvalidBooleanExpression(f'Invalid boolean expression {expression}')
            if op in BINOP_ARIT:
                return ExpBoolean(op,
                        ExpArithmetic.parse(expression[opening+1:closing]),
                        ExpArithmetic.parse(expression[closing+1+len(op):]))
            elif op in BINOP_BOOL:
                return ExpBoolean(op,
                        ExpBoolean.parse(expression[opening+1:closing]),
                        ExpBoolean.parse(expression[closing+1+len(op):]))
        if expression[0] in UNAOP:
            return ExpBoolean(expression[0], ExpBoolean.parse(expression[1:]))
        for i, char in enumerate(expression):
            op = char
            if char in ['<', '>']:
                if i < len(expression) - 1 and expression[i+1] == '=':
                    op += expression[i+1]
            elif i < len(expression) - 1:
                op += expression[i+1]
            j = i+len(op)
            if op in BINOP_ARIT:
                return ExpBoolean(op,
                        ExpArithmetic.parse(expression[:i]),
                        ExpArithmetic.parse(expression[j:]))
            elif op in BINOP_BOOL:
                return ExpBoolean(op,
                        ExpBoolean.parse(expression[:i]),
                        ExpBoolean.parse(expression[j:]))
        return ExpBoolean(expression)

    def __init__(self, op, left=None, right=None):
        Tree.__init__(self)
        self.op = op            # operator or variable str
        self.left = left        # left node ExpBool obj
        self.right = right      # right node ExpBool obj

    def __str__(self, level=0, last=True):
        ret = Tree.__str__(self, level, last)+ " [" + self.op + "]"
        if self.left:
            ret += "\n" + self.left.__str__(level+1, last=(self.right is None))
        if self.right:
            ret += "\n" + self.right.__str__(level+1)
        return ret

    def eval(self, state, catch_vars=None, include_assign=False):
        if self.op in BINOP+UNAOP and catch_vars is not None:
            self.left.eval(state, catch_vars)
            if self.op in BINOP:
                self.right.eval(state, catch_vars)
            return

        if self.op == "true":
            return True
        elif self.op == "false":
            return False
        elif self.op == "||":
            return self.left.eval(state) or self.right.eval(state)
        elif self.op == "&&":
            return self.left.eval(state) and self.right.eval(state)
        elif self.op == "==":
            return self.left.eval(state) == self.right.eval(state)
        elif self.op == "<=":
            return self.left.eval(state) <= self.right.eval(state)
        elif self.op == ">=":
            return self.left.eval(state) >= self.right.eval(state)
        elif self.op == "<":
            return self.left.eval(state) < self.right.eval(state)
        elif self.op == ">":
            return self.left.eval(state) > self.right.eval(state)
        elif self.op == "!=":
            return self.left.eval(state) != self.right.eval(state)
        elif self.op == "!":
            return not self.left.eval(state)
        else:
            if self.op not in state and catch_vars is not None:
                catch_vars.append(self.op)
                return
            return state[self.op]

    # returns opposit boolean expression begining with "!" operator
    def opposit(self):
        return ExpBoolean('!', self)

    # returns string format of expression
    def to_exp(self):
        if self.left and self.right:
            return f"({self.left.to_exp()} {self.op} {self.right.to_exp()})"
        elif self.left and not self.right:
            return f"{self.op}({self.left.to_exp()})"
        return self.op

    # returns list of elementary conditions in expression
    def get_conditions(self):
        conditions = []
        if self.op in BINOP_BOOL + UNAOP:
            conditions.extend(self.left.get_conditions())
            if self.right is not None:
                conditions.extend(self.right.get_conditions())
        elif self.op in BINOP_ARIT:
            return [self]
        return conditions
