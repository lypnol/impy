#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test.Test import Test
from test.AllAssignmentsTest import AllAssignmentsTest
from test.AllConditionsTest import AllConditionsTest
from test.AllDefinitionsTest import AllDefinitionsTest
from test.AllDecisionsTest import AllDecisionsTest
from test.AllILoopsTest import AllILoopsTest
from test.AllKPathsTest import AllKPathsTest
from test.AllUsagesTest import AllUsagesTest
from test.AllDUPathsTests import AllDUPathsTests

TESTS = {
    'TA': AllAssignmentsTest,
    'TD': AllDecisionsTest,
    'TC': AllConditionsTest,
    'k-TC': AllKPathsTest,
    'i-TB': AllILoopsTest,
    'TDef': AllDefinitionsTest,
    'TU': AllUsagesTest,
    'TDU': AllDUPathsTests
}
