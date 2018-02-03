#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def find_bloc_brackets(lines, start=0, bracket='{'):
    opposit = {
        '{': '}',
        '(': ')',
        '[': ']'
    }

    balance = 0
    openning, closing = bracket, opposit[bracket]
    openning_idx, closing_idx = -1, -1
    for i, char in enumerate(lines[start:]):
        if char == openning:
            if balance == 0:
                openning_idx = i
            balance += 1
        elif char == closing:
            balance -= 1
            if balance == 0:
                closing_idx = i
                return openning_idx+start, closing_idx+start
    return -1, -1
