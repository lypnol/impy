#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test.Test import Test


class AllDefinitionsTest(Test):

    def run(self, graph, states):
        raise NotImplementedError

    def generate(self, graph, timeout=10):
        raise NotImplementedError
