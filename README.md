# Impy

IMP language interpreter with formal coverage testing.  
Labeling is optional on programs (see examples).

## Install and usage

impy runs under python 3.6 or higher, install dependencies with pip:
```
pip3 install -r requirements.txt
```

```
usage: im.py [-h]
             [-t {TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} [{TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} ...] | --all-tests]
             [-i INPUT [INPUT ...] | -g] [--timeout TIMEOUT]
             [--k-paths K_PATHS] [--i-loops I_LOOPS] [-cfg CONTROLFLOW]
             source

IMP language interpreter

positional arguments:
  source                Path to source code file

optional arguments:
  -h, --help            show this help message and exit
  -t {TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} [{TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} ...]
                        Runs specific coverage tests
  --all-tests           Runs all available coverage tests
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        Input state set for tests (json files)
  -g, --generate        Generate state set that passes coverage tests
  --timeout TIMEOUT     States generation timeout (seconds)
  --k-paths K_PATHS     Paramter of k-TC test (default 4)
  --i-loops I_LOOPS     Paramter of i-TB test (default 2)
  -cfg CONTROLFLOW, --controlflow CONTROLFLOW
                        Output controlflow graph
```

## Coverage tests

So far, here are the implemented coverage tests:

| Test               	| Flag name 	| Runner 	| Generator 	|
|--------------------	|-----------	|--------	|-----------	|
| AllAssignmentsTest 	| TA        	| OK     	| OK        	|
| AllDecisionsTest   	| TD        	| OK     	| OK        	|
| AllConditionsTest  	| TC        	|        	|           	|
| AllKPathsTest      	| k-TC      	| OK     	| OK        	|
| AllILoopsTest      	| i-TB      	| OK     	| OK        	|
| AllDefinitionsTest 	| TDef      	| OK     	| OK        	|
| AllUsagesTest      	| TU        	| OK       	| OK          	|
| AllDUPathsTests    	| TDU       	|        	|           	|

## Examples

Run IMP program and output its control flow graph
```
$ ./im.py examples/src/prog1.imp -cfg examples/cfg/prog1.imp.png
Control flow graph saved to examples/cfg/prog1.imp.png
Enter initial state
x: 5
Program terminated 0.213 ms.
x: -3
```

Which will result in the following control flow graph

![Control Flow Graph for prog1](https://github.com/lypnol/impy/raw/master/examples/cfg/prog1.imp.png)

Run TA, TD, TDef, k-TC (k = 7) and i-TB (i = 5) tests on prog2.imp against multiple test sets (as json files).
In this example, coverage tests are run against the merged test set of all given test sets, that's why all of them pass.
```
$ ./im.py examples/src/prog2.imp -t TDef TA TD i-TB k-TC --i-loops 5 --k-paths 7 -i examples/tests/prog2/TDef_pass.json examples/tests/prog2/7-TC_pass.json examples/tests/prog2/5-TB_pass.json
AllDefinitionsTest  100.00%
AllAssignmentsTest  100.00%
AllDecisionsTest    100.00%
AllILoopsTest       100.00%
AllKPathsTest       100.00%
```

Generate test set to pass TA, TD and TDef for prog1.imp
```
$ ./im.py examples/src/prog1.imp -t TA TD TDef -g
[
    {
        "x": 99
    },
    {
        "x": 0
    },
    {
        "x": -1
    }
]
```
