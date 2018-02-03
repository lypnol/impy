#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test.Test import Test
from astree.StatementAssign import StatementAssign


class AllAssignmentsTest(Test):

    def run(self, graph, states):
        paths = set()
        for state in states:
            paths.update(set(graph.run(state)))
        for label in graph.get_labels(StatementAssign):
            if label not in paths:
                return False
        return True

    def generate(self, graph, to_pass, timeout=10):
        raise NotImplementedError
