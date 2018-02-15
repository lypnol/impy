#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# main executable script

# stdlib
import argparse
import sys
import json
import time
from copy import deepcopy
# project
from controlflow.ControlFlowGraph import ControlFlowGraph
from test import *


def main():
    parser = argparse.ArgumentParser(description="IMP language interpreter")
    parser.add_argument("source", help="Path to source code file", type=str)
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--tests", nargs="+", help="Runs specific coverage tests", type=str, choices=list(TESTS.keys()))
    group.add_argument("--all-tests", help="Runs all available coverage tests", action="store_true")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--input", nargs="+", help="Input state set for tests (json files)", type=str)
    group.add_argument("-g", "--generate", help="Generate state set that passes coverage tests", action="store_true")

    parser.add_argument("--timeout", help="States generation timeout (seconds)", type=int, default=10)
    parser.add_argument("--k-paths", help="Paramter of k-TC test (default 4)", type=int, default=4)
    parser.add_argument("--i-loops", help="Paramter of i-TB test (default 2)", type=int, default=2)
    parser.add_argument("-cfg", "--controlflow", help="Output controlflow graph", type=str)
    args = parser.parse_args()


    if (args.tests or args.all_tests) and not (args.generate or args.input):
        return print("Cannot run tests without input states. Use -i or -g flag.", file=sys.stderr)

    test_classes = {}
    if args.all_tests:
        test_classes = TESTS
    elif args.tests:
        test_classes = {t: TESTS[t] for t in args.tests}
    
    graph = None
    with open(args.source) as source_file:
        graph = ControlFlowGraph(source_file.read())
    
    if args.controlflow:
        graph.output_graph(args.controlflow)

    if test_classes:
        tests = {}
        for key, test_class in test_classes.items():
            if test_class == AllKPathsTest:
                obj = AllKPathsTest(args.k_paths)
            elif test_class == AllILoopsTest:
                obj = AllILoopsTest(args.i_loops)
            else:
                obj = test_class()
            tests[key] = obj

        states = []
        if args.input:
            for input_file in args.input:
                with open(input_file) as json_file:
                    test_set = json.load(json_file)
                    if test_set is not None:
                        states.extend(test_set)
            states = merge_states(states)
        elif args.generate:
            for coverage_test in tests.values():
                test_set = coverage_test.generate(graph, timeout=args.timeout)
                if test_set is not None:
                    states.extend(test_set)
            states = merge_states(states)
            if not states:
                states = None
            return print(json.dumps(states, indent=4, sort_keys=True))
        
        max_key_len = max(map(lambda x: len(str(x)), tests.keys()))
        max_str_len = max(map(lambda x: len(str(x)), tests.values()))
        for test_name, coverage_test in tests.items():
            coverage = coverage_test.run(graph, deepcopy(states))
            print(f"[{test_name}]", ' '*(max_key_len-len(test_name)),
                coverage_test, ' '*(max_str_len-len(str(coverage_test))),
                '{COLOR}{coverage:6.2f}%{ENDC}'.format(
                    COLOR=('\033[92m' if coverage == 1 else '\033[91m'),
                    ENDC='\033[0m',
                    coverage=coverage*100
            ))
    else:
        state = {}
        print("Enter initial state")
        for var in graph.get_vars():
            state[var] = int(input(f'{var}: '))
        start = time.time()
        state = graph.run(state, return_state=True)
        end = time.time()
        print("Program terminated {:.3f} ms.".format((end-start)*1000))
        for var, value in state.items():
            print(f'{var}: {value}')

if __name__ == '__main__':
    main()
