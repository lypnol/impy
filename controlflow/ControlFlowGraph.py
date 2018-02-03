#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
the ControlFlowGraph of the following example program:
1 : if X <= 0
    then 2 : X := −X;
    else 3 : X := 1 − X;
4 : if X == 1
    then 5 : X := 1;
    else 6 : X := X + 1;

would be:
{
    '1': {
        '2': (ExpBoolean.parse("x <= 0"), StatementSkip()),
        '3': (ExpBoolean.parse("!(x <= 0)"), StatementSkip())
    },
    '2': {
        '4': (ExpBoolean.parse("true"), StatementAssign.parse("x:=-x"))
    },
    '3': {
        '4': (ExpBoolean.parse("true"), StatementAssign.parse("x:=1-x"))
    },
    '4': {
        '5': (ExpBoolean.parse("x == 1"), StatementSkip()),
        '6': (ExpBoolean.parse("!(x == 1)"), StatementSkip())
    },
    '5': {
        ' ': (ExpBoolean.parse("true"), StatementAssign.parse("x:=1"))
    },
    '6': {
        ' ': (ExpBoolean.parse("true"), StatementAssign.parse("x:=x+1"))
    }
}
"""
class ControlFlowGraph:

    def __init__(self, source):
        self.s = {}             # dict statements:  label => statement
        self.g = {}             # dict graph:       label => label => [ExpBool, Statement]
        self.p = {}             # dict parents:     label => label
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

    def build_from_ast(self, ast, return_to=' '):
        start_label = None
        for i, current in enumerate(ast.sequence):
            goto = return_to if i == len(ast.sequence)-1 else ast.sequence[i+1].label
            
            self.add_node(current)

            if i == 0:
                start_label = current.label
                if self.start is None:
                    self.start = current.label

            if isinstance(current, StatementAssign):
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

    def run(self, state, return_state=False):
        curr = self.start
        path = []
        while curr != ' ':
            path.append(curr)
            for child, (exp, statement) in self.g[curr].items():
                if exp.eval(state):
                    statement.eval(state)
                    curr = child
        if return_state:
            return state
        return path

    def get_vars(self):
        catch_vars = []
        self.ast.eval({}, catch_vars=catch_vars)
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

    def get_paths(self, max_length=0, max_whiles=0):
        raise NotImplementedError


if __name__ == "__main__":
    cfg = ControlFlowGraph("""
1 : if (X <= 0) {
    2 : X := -X;
} else {
    3 : X := 1 - X;
}
4 : if (X == 1) {
    5 : X := 1;
} else {
    6 : X := X + 1;
}
""")
#     cfg = ControlFlowGraph("""
# 0 : X := 2;
# 1 : if (X <= 0) {
#     2 : X := -X;
# } else {
#     3 : X := 1 - X;
# }
# 4 : if (X == 1) {
#     5 : X := 1;
#     6 : X := X + 1;
# }
# 7 : Y := 5;
# 8 : while Y + X >= X    
# {
#     9 : Y := X - Y;
#     10 : X := Y + X;
#     11 : if ((X < 2) && (1 >= 0)) || true {
#         12 : var := 4*3;
#         13: if X > 0 {
#             14: X := X;
#         }
#     }
# }
#     """)

    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.DiGraph()
    for u in cfg.g:
        if u == cfg.start:
            G.add_node(u, label=u, fillcolor='white', rank=0)
        else:
            G.add_node(u, label=u, fillcolor='white')
    for u, connections in cfg.g.items():
        for v, edge in connections.items():
            print(u, "->", v)
            print(edge[0])
            print(edge[1])
            G.add_edge(u, v, label=f'{edge[0].__class__.__name__} {edge[1].__class__.__name__}')

    nx.draw(G, pos=nx.spring_layout(G))
    plt.axis("off")
    plt.show()
