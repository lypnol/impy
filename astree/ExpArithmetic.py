#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from astree.Tree import Tree
from astree.utils import find_bloc_brackets


BINOP = ['+', '-', '*', '%']
UNAOP = ['-']

class InvalidArithmeticExpression(Exception): pass

class ExpArithmetic(Tree):
    
    @staticmethod
    def parse(expression):
        if expression == '':
            return None
        # remove all whitespace characters
        expression = ''.join(expression.split())
        if expression[0] == '(':
            opening, closing = find_bloc_brackets(expression, bracket='(')
            if closing == -1:
                raise InvalidArithmeticExpression(f'Invalid arithmetic expression {expression}')
            if closing == len(expression):
                return ExpArithmetic.parse(expression[opening+1:closing])
            op = expression[closing+1]
            if op not in BINOP:
                raise InvalidArithmeticExpression(f'Invalid arithmetic expression {expression}')
            return ExpArithmetic(op,
                    ExpArithmetic.parse(expression[opening+1:closing]),
                    ExpArithmetic.parse(expression[opening+1+len(op):closing]))
        if expression[0] in UNAOP:
            return ExpArithmetic(expression[0], ExpArithmetic.parse(expression[1:]))
        for i, char in enumerate(expression):
            if char in BINOP:
                return ExpArithmetic(char,
                        ExpArithmetic.parse(expression[:i]),
                        ExpArithmetic.parse(expression[i+1:]))
        return ExpArithmetic(expression)

    def __init__(self, op, left=None, right=None):
        Tree.__init__(self)
        self.op = op
        self.left = left
        self.right = right

    def __str__(self, level=0, last=True):
        ret = Tree.__str__(self, level, last)+ " [" + self.op + "]"
        if self.left:
            ret += "\n" + self.left.__str__(level+1, last=(self.right is None))
        if self.right:
            ret += "\n" + self.right.__str__(level+1)
        return ret

    def eval(self, state, catch_vars=None):
        if self.op in BINOP+UNAOP and catch_vars is not None:
            self.left.eval(state, catch_vars)
            if self.right:
                self.right.eval(state, catch_vars)
            return

        if self.op == '+':
            return self.left.eval(state) + self.right.eval(state)
        elif self.op == '-':
            if self.right:
                return self.left.eval(state) - self.right.eval(state)
            else:
                return -self.left.eval(state)
        elif self.op == '*':
            return self.left.eval(state) * self.right.eval(state)
        elif self.op == '%':
            return self.left.eval(state) % self.right.eval(state)
        try:
            return int(self.op)
        except ValueError:
            if self.op not in state and catch_vars is not None:
                catch_vars.append(self.op)
                return
            return state[self.op]

    def to_exp(self):
        if self.left and self.right:
            return f"({self.left.to_exp()} {self.op} {self.right.to_exp()})"
        elif self.left and not self.right:
            return f"{self.op}{self.left.to_exp()}"
        return self.op