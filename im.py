#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# stdlib
import argparse
import sys
import json
import time
# project
from controlflow import ControlFlowGraph
from test import *


def main():
    parser = argparse.ArgumentParser(description="IMP language interpreter")
    parser.add_argument("source", help="Path to source code file", type=str)
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--tests", nargs="+", help="Runs specific coverage tests", type=str, choices=list(TESTS.keys()))
    group.add_argument("--all-tests", help="Runs all available coverage tests", action="store_true")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--input", help="Input state set for tests (json file)", type=str)
    group.add_argument("-gp", "--generate-pass", help="Generate state set that passes coverage tests", action="store_true")
    group.add_argument("-gf", "--generate-fail", help="Generate state set that fails coverage tests", action="store_true")

    parser.add_argument("--timeout", help="States generation timeout (seconds)", type=int, default=10)
    parser.add_argument("--k-paths", help="Paramter of k-TC test", type=int, default=3)
    parser.add_argument("--i-loops", help="Paramter of i-TB test", type=int, default=1)
    args = parser.parse_args()


    if (args.tests or args.all_tests) and not (args.generate_pass or args.generate_fail or args.input):
        return print("Cannot run tests without input states. Use -i, -gp or -gf flags.", file=sys.stderr)

    if (args.generate_pass or args.generate_fail) and not args.tests:
        return print("Generate flag can only be used with --test flag.", file=sys.stderr)    

    test_types = None
    if args.all_tests:
        test_types = list(TESTS.values())
    elif args.tests:
        test_types = [TESTS[t] for t in args.tests]
    
    graph = None
    with open(args.source) as source_file:
        graph = ControlFlowGraph(source_file.read())
    # print(graph.source)

    if test_types:
        tests = []
        for test_type in test_types:
            if test_type == AllKPathsTest:
                obj = AllKPathsTest(args.k_paths)
            elif test_type == AllILoopsTest:
                obj = AllILoopsTest(args.i_loops)
            else:
                obj = test_type()
            tests.append(obj)
        
        if args.input:
            with open(args.input) as json_file:
                states = json.load(json_file)
        elif args.generate_pass or args.generate_fail:
            coverage_test = tests[0]
            states = coverage_test.generate(graph, args.generate_pass, timeout=args.timeout)
            return print(json.dumps(states, indent=2, sort_keys=True))
        
        for coverage_test in tests:
            passed = coverage_test.run(graph, states)
            print(coverage_test, '{COLOR}{status}{ENDC}'.format(
                COLOR=('\033[92m' if passed else '\033[91m'),
                ENDC='\033[0m',
                status=('pass' if passed else 'failed')
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
