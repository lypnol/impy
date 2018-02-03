#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Abstract test class
"""
class Test:

    def run(self, graph, states):
        raise NotImplementedError
    
    def generate(self, graph, to_pass, timeout=10):
        raise NotImplementedError
    
    def __repr__(self):
        return repr(str(self))
    
    def __str__(self):
        return self.__class__.__name__
