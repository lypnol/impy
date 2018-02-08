#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def merge_states(states):
    test_set = set()
    for state in states:
        test_set.add(frozenset(state.items()))
    return [{k: v for k, v in state} for state in test_set]
