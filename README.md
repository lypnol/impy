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
             [-t {TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} [{TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} ...]
             | --all-tests] [-i INPUT | -g] [--timeout TIMEOUT]
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
  -i INPUT, --input INPUT
                        Input state set for tests (json file)
  -g, --generate        Generate state set that passes coverage tests
  --timeout TIMEOUT     States generation timeout (seconds)
  --k-paths K_PATHS     Paramter of k-TC test
  --i-loops I_LOOPS     Paramter of i-TB test
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
| AllUsagesTest      	| TU        	|        	|           	|
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

Run AllAssignmentsTest on prog1.imp:
```
$ ./im.py examples/src/prog1.imp -t TA -i examples/tests/prog1/TA_pass.json
AllAssignmentsTest  100.00%
```

Generate data set to pass AllAssignmentsTest for prog1
```
$ ./im.py examples/src/prog1.imp -t TA -g
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
