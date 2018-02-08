#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# stdlib
import sys
# 3p
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
# project
from astree.AST import AST
from astree.ExpArithmetic import ExpArithmetic
from astree.ExpBoolean import ExpBoolean
from astree.StatementSequence import StatementSequence
from astree.StatementAssign import StatementAssign
from astree.StatementSkip import StatementSkip
from astree.StatementIf import StatementIf
from astree.StatementWhile import StatementWhile


"""
ControlFlowGraph represents a program's control flow graph.
"""
class ControlFlowGraph:

    def __init__(self, source):
        self.s = {}             # dict statements:  label => statement
        self.g = {}             # dict graph:       label => label => [ExpBool, Statement]
        self.p = {}             # dict parents:     label => [label]
        self.start = None       # starting node

        self.source = AST.preprocess(source)
        self.ast = AST.parse(self.source)
        self.build_from_ast(self.ast)

    def add_node(self, statement):
        label = statement.label
        self.s[label] = statement
        self.g[label] = {}

    def add_edge(self, a, b, expbool, statement):
        self.g[a][b] = [expbool, statement]
        if b not in self.p:
            self.p[b] = [a]
        else:
            self.p[b].append(a)

    def get_statement(self, u):
        return self.s[u]

    def get_edge(self, u, v):
        return self.g[u][v]

    def build_from_ast(self, ast, return_to=' '):
        start_label = None
        for i, current in enumerate(ast.sequence):
            goto = return_to if i == len(ast.sequence)-1 else ast.sequence[i+1].label
            
            self.add_node(current)

            if i == 0:
                start_label = current.label
                if self.start is None:
                    self.start = current.label

            if isinstance(current, StatementAssign) or isinstance(current, StatementSkip):
                self.add_edge(current.label, goto, ExpBoolean("true"), current)
            
            elif isinstance(current, StatementIf):
                start = self.build_from_ast(current.statement_t, goto)
                self.add_edge(current.label, start, current.exp, StatementSkip())
                if current.statement_f:
                    start = self.build_from_ast(current.statement_f, goto)
                    self.add_edge(current.label, start, current.exp.opposit(), StatementSkip())
                else:
                    self.add_edge(current.label, goto, current.exp.opposit(), StatementSkip())
            
            elif isinstance(current, StatementWhile):
                start = self.build_from_ast(current.statement, current.label)
                self.add_edge(current.label, start, current.exp, StatementSkip())
                self.add_edge(current.label, goto, current.exp.opposit(), StatementSkip())
                
        return start_label

    def run(self, state, return_state=False, max_length=-1, max_whiles=-1):
        curr = self.start
        path = []
        while curr != ' ':
            if (max_length > -1) and len(path) == max_length:
                break
            if (max_whiles > -1) and (max_whiles == 0 and isinstance(self.s[curr], StatementWhile)):
                break
            path.append(curr)
            if isinstance(self.s[curr], StatementWhile):
                max_whiles -= 1
            for child, (exp, statement) in self.g[curr].items():
                if exp.eval(state):
                    statement.eval(state)
                    curr = child
        if not ((max_length > -1) and len(path) == max_length):
            path.append(curr)
        if return_state:
            return state
        return tuple(path)

    def get_vars(self, include_assign=False):
        catch_vars = []
        self.ast.eval({}, catch_vars=catch_vars, include_assign=include_assign)
        return set(catch_vars)
    
    def get_labels(self, *classtypes):
        res = set()
        if not classtypes:
            classtypes = [StatementAssign, StatementIf, StatementSkip, StatementWhile]
        for label, statement in self.s.items():
            if any(isinstance(statement, statement_class) for statement_class in classtypes):
                res.add(label)
        return res

    def get_edges_from(self, *classtypes):
        res = set()
        if not classtypes:
            classtypes = [StatementAssign, StatementIf, StatementSkip, StatementWhile]
        for u in self.g:
            if any(isinstance(self.s[u], statement_class) for statement_class in classtypes):
                for v, edge in self.g[u].items():
                    res.add((u, v))
        return res

    def get_edges_to(self, *classtypes):
        res = set()
        classtypes = [StatementAssign, StatementIf, StatementSkip, StatementWhile] if not classtypes else classtypes
        for u in self.g:
            if u == ' ':
                continue
            if any(isinstance(self.s[u], statement_class) for statement_class in classtypes):
                for p in self.p[u]:
                    res.add((p, u))
        return res

    def get_paths_to(self, node, suffix=[]):
        suffix = [node]+suffix
        if node not in self.p or node == self.start:
            return [tuple(suffix)]
        paths = []
        for parent in self.p[node]:
            if parent not in suffix:
                paths.extend(self.get_paths_to(parent, suffix))
        return paths

    def get_paths(self, max_length=-1, max_whiles=-1, node=None, prefix=[]):
        node = self.start if node is None else node
        prefix = prefix+[node]
        if node == ' ':
            return [tuple(prefix)]
        if max_length == 0 or max_whiles == 0:
            return []
        paths = []
        for v in self.g[node]:
            if ((max_length <= -1 and max_whiles <= -1) and v not in prefix) or \
            not (max_length <= -1 and max_whiles <= -1):
                if isinstance(self.s[node], StatementWhile):
                    max_whiles -= 1
                paths.extend(self.get_paths(max_length-1, max_whiles, v, prefix))
        return paths

    def is_def(self, u, x):
        statement = self.s[u]
        return isinstance(statement, StatementAssign) and statement.var == x

    def ref(self, u):
        statement = self.s[u]
        catched_vars = []
        if isinstance(statement, StatementWhile) or isinstance(statement, StatementIf):
            statement.exp.eval({}, catched_vars)
        elif isinstance(statement, StatementAssign):
            statement.arithmetic_exp.eval({}, catched_vars)

        return set(catched_vars)

    def output_graph(self, output):
        G = nx.DiGraph()
        for u in self.g:
            G.add_node(u, label=u, fillcolor='white', labelfontsize=22)
        for u, connections in self.g.items():
            for v, edge in connections.items():
                G.add_edge(u, v, label=f'{edge[0].to_exp()}\n{edge[1].to_exp()}', fontsize=9)

        A = to_agraph(G)
        A.layout('dot')
        A.draw(output)
        print(f"Control flow graph saved to {output}", file=sys.stderr)
